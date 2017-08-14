//////////////////////////////////////////////// JQUERY 
$(document).ready(function() {
// ADMIN PROFILE
    $('#btn_approve_all_sections').click(function() {
        if (!confirm('Вы уверены?')) {
            return false
        }
        var $save_result_div = $("#div_all_sections_approve")
        var post_data = { 
                         'user_id'   : $("#user_id").val(),
                         'do'        : 'approve_all_sections',
                        }
        $.ajax({
            type: 'post',
            url: '/post_query',
            data: post_data,
            success: function (res) {
                var msg = res['message']
                $save_result_div.removeClass('no-display')
                if (!$save_result_div.hasClass('alert-success')) {
                    $save_result_div.addClass('alert-success')
                }
                $.each( ['.status_span'], function( index, value ) {
                    if (! $(value).parent('.admin_section')) {
                        $( value ).replaceWith('<span class="status_span alert-success" style="float:right">&nbsp одобрено &nbsp</span>')
                    }
                })
                $save_result_div.text('все секции одобрены')
            },
            dataType: 'json',
            async: true,
        });
        return false
    });


    $('.btn_change_section_state').click(function() {
        
        var approved = $(this).hasClass('approved')
        var new_state = $(this).attr('data')
        var $section = $(this).closest('.section');
        var $status_span = $section.find('.status_span');
        var $save_result_div = $section.find('.save_result_div');
        var post_data = { 
                         'user_id'   : $("#user_id").val(),
                         'new_state' : new_state,
                         'comment'   : $section.find(".section_comment").val(),
                         'table'     : $section.find("input[name='table']").val(),
                         'do'        : 'change_section_state',
                        };

        $.ajax({
            type: 'post',
            url: '/post_query',
            data: post_data,
            success: function (res) {
                var msg = res['message']
                $save_result_div.removeClass('no-display')
                if (approved) {
                    $status_span.replaceWith('<span class="status_span alert-success" style="float:right">&nbsp одобрено &nbsp</span>')
                    $save_result_div.removeClass('alert-danger')
                    if (!$save_result_div.hasClass('alert-success')) {
                        $save_result_div.addClass('alert-success')
                    }
                    $save_result_div.text('секция одобрена')
                } else {
                    $status_span.replaceWith('<span class="status_span alert-danger" style="float:right">&nbsp отклонено &nbsp</span>')
                    $save_result_div.removeClass('alert-success')
                    if (!$save_result_div.hasClass('alert-danger')) {
                        $save_result_div.addClass('alert-danger')
                    }
                    $save_result_div.text('секция отклонена')
                }
            },
            dataType: 'json',
            async: true,
        });
        return false;
    });
// **************

// selectors hardcode
    function set_and_fix_input_field(text, name, value) {
        var p_name = text.indexOf('name="'+name+'"') + ('name="'+name+'"').length
        var p_value = text.indexOf('value="', p_name) + 'value="'.length
        return text.substring(0, p_name) + ' readonly="readonly" ' + 
               text.substring(p_name, p_value) + value +
               text.substring(p_value)
    }

    function copy_template_with_replace(selector, name, value) {
        var $parent = $(selector).closest('form')
        $parent.find('.no-elements').remove()
        var $template = $parent.find(".section_element_template_div")
        var element_html = "<div class='well well-lg not_fixed_element'>" + set_and_fix_input_field($template.html(), name, value) + "</div>"
        $parent.find('.place_to_insert_element').before(element_html)
        
        return false;
    }

    $('#btn_add_section_element_son').click(function() {
        copy_template_with_replace($(this), 'status', 'Сын')   
    });

    $('#btn_add_section_element_daughter').click(function() {
        copy_template_with_replace($(this), 'status', 'Дочь')   
    });

    $('#btn_add_section_element_brother').click(function() {
        copy_template_with_replace($(this), 'status', 'Брат')   
    });

    $('#btn_add_section_element_sister').click(function() {
        copy_template_with_replace($(this), 'status', 'Сестра')   
    });

    $('#btn_add_section_element_bachelor').click(function() {
        if ($(this).closest('form').html().indexOf('Бакалавриат') != -1) {
            alert("Вы уже добавили бакалавриат")
        } else {
            copy_template_with_replace($(this), 'quality', 'Бакалавриат')   
        }
    });

    $('#btn_add_section_element_master').click(function() {
        if ($(this).closest('form').html().indexOf('Магистратура') != -1) {
            alert("Вы уже добавили магистратуру")
        } else {
            copy_template_with_replace($(this), 'quality', 'Магистратура')  
        } 
    });

    $('#btn_add_section_element_phd').click(function() {
        if ($(this).closest('form').html().indexOf('Аспирантура') != -1) {
            alert("Вы уже добавили аспирантуру")
        } else {
            copy_template_with_replace($(this), 'quality', 'Аспирантура')
        }
    });

    $('#btn_add_section_element_mother').click(function() {
        if ($(this).closest('form').html().indexOf('Мать') != -1) {
            alert("Вы уже добавили мать")
        } else {
            copy_template_with_replace($(this), 'status', 'Мать')
        }   
    });

    $('#btn_add_section_element_father').click(function() {
        if ($(this).closest('form').html().indexOf('Отец') != -1) {
            alert("Вы уже добавили отца")
        } else {
            copy_template_with_replace($(this), 'status', 'Отец')
        }  
    });


// selectors hardcode end

    $('.btn_add_section_element').click(function() {
        var $parent = $(this).closest('form')
        $parent.find('.no-elements').remove()
        var $template = $parent.find(".section_element_template_div")
        var element_html = "<div class='well well-lg not_fixed_element'>" + $template.html() + "</div>"
        $(this).before(element_html)
        
        return false; 
    });

    $(document).on('click', '.btn_remove_not_fixed_element', function(){
        $(this).closest('.not_fixed_element').remove();
        return false;
    });

    $('form.section_form').submit(function() {
        var $inputs = $(this).find(':input');
        var $section = $(this).closest('.section');
        var $status_span = $section.find('.status_span');
        var $save_result_div = $(this).find('.save_result_div');
        
        var post_data = { 'user_id' : $("#user_id").val() };
        var data_sections = [];
        var data_buffer = {};
        var is_not_fixed = $(this).parents('div.not_fixed_section').length;
        var cnt_elements = 0;
        var is_inside_element = false;
        $inputs.each(function() {
            if ($(this).parents('.section_element_template_div').length > 0) {
                return;
            }
            if (is_not_fixed) {
                if (this.name == 'new_element_end') {
                    if (Object.keys(data_buffer).length > 0) {
                        data_sections.push( $.extend({}, data_buffer) );
                        cnt_elements++;
                        data_buffer = {};
                    }    
                    is_inside_element = false;
                } else 
                if (this.name == 'new_element_start') {
                    is_inside_element = true;

                } else if (is_inside_element) {
                    data_buffer[this.name] = $(this).val();
                } else {
                    post_data[this.name] = $(this).val();   
                }
            } else {
                post_data[this.name] = $(this).val();
            }
        });
        if (is_not_fixed) {
            post_data['elements'] = JSON.stringify(data_sections);
        }
        $.ajax({
            type: 'post',
            url: '/post_query',
            data: post_data,
            success: function (res) {
                var msg = res['message']
                $save_result_div.removeClass('no-display')
                if (msg['status'] == 'ok') {
                    $status_span.replaceWith('<span class="status_span alert-info" style="float:right">&nbsp на проверке &nbsp</span>')
                    $save_result_div.removeClass('alert-danger')
                    if (!$save_result_div.hasClass('alert-info')) {
                        $save_result_div.addClass('alert-info')
                    }
                    $save_result_div.text('изменения сохранены')
                } else {
                    $save_result_div.removeClass('alert-info')
                    if (!$save_result_div.hasClass('alert-danger')) {
                        $save_result_div.addClass('alert-danger')
                    }
                    $save_result_div.html(msg['errors'])
                }
            },
            dataType: 'json',
            async: true,
        });
        return false;
    });

//SEARCH

    $('#search-btn').click(function() {
        var data = {
            'do': 'searchUsers',
            'lastName': $('#searchLastname').val(),
            'year': $('#searchYear').val(),
            'vus': $('#searchVus').val(),
            'is_approved': 0,
        }
        if ($('#searchIsApproved') && $('#searchIsApproved').prop('checked')) {
            data['is_approved'] = 1
        } 

        $('#user-search-result > tbody').empty()

        $.ajax({
            type: 'post',
            url: 'post_query',
            data: data,
            success: function (res) {
                var userData = res['result']
                if (userData.length) {
                    $('#div_empty_result').text('')
                    for (i in userData) {
                        var rowHtml = '<tr>' + 
                        '<td>' + userData[i]['lastName'] + '</td>' +
                        '<td>' + userData[i]['year'] + '</td>' +
                        '<td>' + userData[i]['vus'] + '</td>' +
                        '<td>' + userData[i]['is_approved'] + '</td>' +
                        '<td>' + '<a href="/inprocess/'+userData[i]['id']+'">' + 
                        "<button type='button' class='btn btn-primary btn-show-from-search' data-id=" + userData[i]['id'] + 
                        '>Показать</button></a></td>' + 
                        '</tr>';
                        $('#user-search-result > tbody:last-child').append(rowHtml);
                    }
                } else {
                    $('#div_empty_result').text('Результат поиска пуст')
                }
            },
            dataType: 'json',
            async: false,
        });
    });

    $('#search-btn-ready').click(function() {
        var data = {
            'do': 'searchUsers',
            'lastName': $('#searchLastname').val(),
            'year': $('#searchYear').val(),
            'vus': $('#searchVus').val(),
            'is_approved': 1,
        }

        $('#user-search-result > tbody').empty();


        $.ajax({
            type: 'post',
            url: 'post_query',
            data: data,
            success: function (res) {
                var userData = res['result']
                if (userData.length) {
                    $('#div_empty_result').text('')
                    for (i in userData) {
                        var rowHtml = '<tr>' +
                        '<td>' + "<input type='checkbox' class='cb-user' value='" + userData[i]['id'] + "'>" + '</td>' +
                        '<td>' + userData[i]['year'] + '</td>' +
                        '<td>' + userData[i]['vus'] + '</td>' +
                        '<td>' + userData[i]['lastName'] + '</td>' +
                        '<td>' + userData[i]['firstName'] + '</td>' +
                        '<td>' + userData[i]['middleName'] + '</td>' +
                        '<td>' + '<a href="/inprocess/' + userData[i]['id'] + '"> <button type="button" class="btn btn-default">Посмотреть</button></a><' + '/td>' +
                        '</tr>';
                        
                        $('#user-search-result > tbody:last-child').append(rowHtml);
                    }
                } else {
                    $('#div_empty_result').text('Результат поиска пуст')
                }
            },
            dataType: 'json',
            async: false,
        });
    });

    $(document).on('click', '.btn-show-from-search', function(){
        var id = $(this).data('id')
    })

/// READY 

    $('#checkallUsers').change(function() {
        $('.cb-user').prop( 'checked', this.checked )
    })

    $('#checkallDocuments').change(function() {
        $('.cb-doc').prop( 'checked', this.checked)
    })

    $('#generateBtn').click(function() {
        var input_date = prompt('Введите дату генерации документов (дд.мм.гггг):')
        if (! /^\d\d\.\d\d\.\d{4}$/.test(input_date)) {
            alert('Неверный формат даты, требуется дд.мм.гггг')
            return false;
        }

        var checkedCbUsers = $('.cb-user:checkbox:checked')
        var checkedCbDocs = $('.cb-doc:checkbox:checked')

        var userIDs = checkedCbUsers.map(function() {
            return this.value
        }).get()
        var docIDs = checkedCbDocs.map(function() {
            return this.value
        }).get()

        var data = {
            'do' : 'generateDocuments',
            'userIDs' : JSON.stringify(userIDs),
            'docIDs' : JSON.stringify(docIDs),
            'generation_date' : input_date,
        }

        $(this).html('Генерация...')
        $('#downloadBtn').prop('disabled', true)

        $.ajax({
            type: 'post',
            url: 'post_query',
            data: data,
            success: function (res) {
                $('#generateBtn').html('Сгенерировать')
                if (res['success'] == true) {
                    $('#downloadHref').prop('href', res['url'])
                    $('#downloadHref').prop('download', 'Documents')
                    $('#downloadBtn').prop('disabled', false)
                } else {
                    console.log(res)
                    alert(res['message'])
                }
            },
            dataType: 'json',
            async: false
        });
    });
    
/// Create admin account
    $('input[type=radio][name=type_admin]').change(function() {
        if (this.value == 'admin_vus') {
            $('#vus_for_admin').prop('disabled', false);
        }
        else  {
            $('#vus_for_admin').prop('disabled', true);
        }
    });

    $('#create-but-1').click(function() {
        if( $("#login").val()=='' || $("#password").val()=='' ){
            alert('Не заполены "Логин" и/или "Пароль"')
            return false
        }
        var post_data = { 
                         'login'    : $("#login").val(),
                         'password' : $("#password").val(),
                        }

        if( $('#admin_readonly').is(':checked') ){
            post_data['role'] = 'ROLE_READONLY_ADMIN';
            post_data['vus_id'] = '-1';
        }
        else{
            post_data['role'] = 'ROLE_ADMIN';
            post_data['vus_id'] = $("#vus_for_admin").val();
        }

        $.ajax({
            type: 'post',
            url: '/make_account',
            data: post_data,
            success: function (res) {
                var msg = res['message'];
                if(msg['status'] == 'ok'){
                    alert('Аккаунт успешно создан')
                }
                else{
                    alert(msg['error'])
                }
            },
            dataType: 'json',
            async: true,
        });
        return false
    });

/// add vus
    $('#add_vus_btn').click(function() {
        if( $("#number").val()=='' || $("#code").val()=='' 
            || $("#name1").val()=='' || $("#name2").val()=='' ){
            alert('Заполните все поля')
            return false
        }
        var post_data = { 
                         'number'   : $("#number").val(),
                         'code'     : $("#code").val(),
                         'name1'    : $("#name1").val(),
                         'name2'    : $("#name2").val(),
                        }

        $.ajax({
            type: 'post',
            url: '/post_add_vus',
            data: post_data,
            success: function (res) {
                var msg = res['message'];
                if(msg['status'] == 'ok'){
                    alert('ВУС успешно добавлена')
                }
                else{
                    alert(msg['error'])
                }
            },
            dataType: 'json',
            async: true,
        });
        return false
    });

/// Consent to processing personal data
    $('#consent_proc').click(function(){
        if($('#consent_proc').is(':checked')){
            $('#btn_continue').prop('disabled', false)
        }
        else{
            $('#btn_continue').prop('disabled', true)
        }
    });

    $('#btn_continue').click(function(){
        if($('#consent_proc').is(':checked')){
            $.ajax({
                type: 'post',
                url: '/consent_proc',
                success: function (res) {
                    var msg = res['message'];
                    if(msg['status'] == 'ok'){
                        alert('Соглашение оформлено')
                        location.reload()
                    }
                    else{
                        alert(msg['error'])
                    }
                },
                async: true,
            });
        }
        else{
            alert('Вы не дали согласие')
        }
    });
});

/////////////////////////////////////////////////

/**
 * Created by User on 08.08.2016.
 */
if(typeof(String.prototype.trim) === "undefined") {
    String.prototype.trim = function() {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}


function changeLoginStatus(text, color){
    var status = document.getElementById('login-status');
    status.style.color = color;
    status.innerHTML = text;
    status.style.display = 'block';
}

function getXHR(){
    var xmlhttp;
    if (window.XMLHttpRequest){ xmlhttp = new XMLHttpRequest(); }
    else { xmlhttp = new ActiveXObject("Microsoft.XMLHTTP"); }
    return xmlhttp;
}

function complexXHR(url, params, changeStatus, valueSet, onSuccess){
    var xmlhttp = getXHR();
    if (valueSet == 0){
        valueSet = {before: 'Подождите...', serverError: 'Ошибка сервера', resultError: 'Неправильный ответ сервера'};
    }

    changeStatus(valueSet.before, 0);

    xmlhttp.open("POST", url, true);
    xmlhttp.onerror = function (e) {
        changeStatus(valueSet.serverError, 1);
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == 'error'){
                changeStatus(ans.message, 1);
            } else {
                onSuccess(ans);
            }
        } else {
            changeStatus(valueSet.before, 1);
        }
    };
    xmlhttp.send(JSON.stringify(params));
}

function logout(){
    var xmlhttp = getXHR();

    xmlhttp.open("POST", "/logout", true);
    xmlhttp.onerror = function (e) {
        //alert('server error');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            location.reload();
        }
    };

    xmlhttp.send();
}

function dologin(){
    var params = {
        login: document.getElementById('login').value,
        password: document.getElementById('password').value
    };
    complexXHR('/login', params, function (message, error) {
        changeLoginStatus(message, '#black');
    }, 0,
        function(ans){
            location.reload();
        }
    );
}

function pressEnter( e ){
    if (e.keyCode == 13)
    {
        dologin();
        return false;
    }
    return true;
} 

function createAccounts(){
    var xmlhttp = getXHR();
    var file = document.getElementById('select-file').files[0];
    var vus = document.getElementById('vus').value;
    var completionYear = document.getElementById('completionYear').value;
    var btn = document.getElementById('status-btn');
    var downloadBtn = document.getElementById('downloadLoginsBtn');

    downloadLoginsBtn.disabled = true

    var formData = new FormData();
    formData.append('file', file);
    formData.append('vus', vus);
    formData.append('completionYear', completionYear);
    xmlhttp.open("POST", "/create_accounts", true);
    xmlhttp.onerror = function (e) {
        btn.innerText('server error');
    };
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);
            var placeholder = document.getElementById('alert-placeholder')

            if (ans.status == 'error'){
                placeholder.removeChild(placeholder.firstChild)

                var alert = document.createElement('div')

                alert.innerHTML = '<div class="alert alert-danger" role="alert">' +
                    '<strong>Ошибка </strong>' +
                    ans.message +
                    '</div>';

                placeholder.appendChild(alert);
            } else {
                downloadLoginsBtn.disabled = false
                //download(ans.url, 'logins.xlsx')
                //location.reload();
            }
        }
    };

    xmlhttp.send(formData);
}


function addDocument(){
    var xmlhttp = getXHR();
    var file = document.getElementById('select-file').files[0];
    var name = document.getElementById('doc_name').value;
    var vus = document.getElementById('vus').value;
    var btn = document.getElementById('status-btn');

    var formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('vus', vus);

    xmlhttp.open("POST", "/add_document", true);
    xmlhttp.onerror = function (e) {
        btn.innerText('server error');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == "error"){
                btn.innerText = ans.message;
            } else {
                location.reload();
            }
        }
    };

    xmlhttp.send(formData);
}


function generate(functionOnSuccess){
    var xmlhttp = getXHR(), i;
    var usersCB = document.getElementsByClassName('cb-user');
    var docsCB = document.getElementsByClassName('cb-doc');

    var users = [],
        docs = [];

    for (i = 0; i < usersCB.length; i++){
        if (usersCB[i].checked){
            users.push(+usersCB[i].id.substr(3));
        }
    }

    for (i = 0; i < docsCB.length; i++){
        if (docsCB[i].checked){
            docs.push(+docsCB[i].id.substr(3));
        }
    }

    var params = {
        users: users,
        documents: docs
    };

    document.getElementById('gen-button').innerHTML = 'Генерация...';

    xmlhttp.open("POST", "/generate_documents", true);  //TODO: Realize this request
    xmlhttp.onerror = function (e) {
        // TODO: Server error.
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById('gen-button').innerHTML = '1';
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == 'ERROR'){
                // TODO: Error on input data
            } else {
                document.getElementById('gen-button').innerHTML = 'Сгенерировать и скачать';
                //docpath = ans.url;
                //document.getElementById('gen-button').innerHTML = ans.url;
                functionOnSuccess(ans.url);
            }
        }
    };
    xmlhttp.send(JSON.stringify(params));
}

function download(url, renameTo){
    var element = document.createElement('a');
    element.setAttribute('href', url);
    element.setAttribute('download', renameTo);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function genAndDownload(){
    generate(function(url){ download(url, 'Documents.zip'); });
}

function prepareFileUploader(idName){
    var input = document.getElementById(idName);
    var label = input.parentElement;
    var filename = '';

    input.onclick = function () {
        this.value = null;
        this.classList.remove('file-selected');
    };

    input.onchange = function () {
        this.classList.add('file-selected');
        filename = this.value;
        label.getElementsByTagName('div')[0].innerHTML = 'OK';
    };
}

function delDoc(docId){
    var xmlhttp = getXHR();
    var params = {
        docId: docId
    };

    //var btn = document.getElementById('status-btn');

    //location.reload();      // TODO: DELETE THIS!

    xmlhttp.open("POST", "/delete_document", true);
    xmlhttp.onerror = function (e) {
        //btn.innerText('serverError');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            location.reload();
        }
    };

    xmlhttp.send(JSON.stringify(params));
}

///////////////////////////

function sleep (time) {
    return new Promise(function(resolve){setTimeout(resolve, time)});
}



