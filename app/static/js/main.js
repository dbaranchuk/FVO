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

function submitStudentInfo(fields){
    var params = {};
    for(var i in fields){
        if(document.getElementById(fields[i]) != null){
            params[fields[i]] = document.getElementById(fields[i]).value;
        }
    }

    var relatives = ['who-', 'last-name-', 'first-name-', 'middle-name-',
                        'phones-', 'address-usual-', 'address-registration-']
    
    var c_relat = 0;
    var flag_get_relat = false;
    for(var i = 1; i < count_relatives+1; i ++){
        for(var j in relatives){
            if(document.getElementById(relatives[j] + i)){
                flag_get_relat = true;
                params[relatives[j] + c_relat] = document.getElementById(relatives[j] + i).value;
            }
        }
        if(flag_get_relat){
            c_relat++;
        }
        flag_get_relat = false;
    }

    params['count_relatives'] = c_relat;

    var xmlhttp = getXHR();
    var formData = new FormData();
    for(var i in params){
        formData.append(i,params[i]);
    }

    xmlhttp.open("POST", "/add_data", true);
    xmlhttp.onerror = function (e) {
        //alert('server error');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == 'ERROR'){
                btn.innerText(ans.message);
            } else {
                location.reload();
            }
        }
    };

    xmlhttp.send(formData);
}

function submitApprove(user_id){
    var params = {};
    params['id'] = user_id;

    var xmlhttp = getXHR();
    var formData = new FormData();
    for(var i in params){
        formData.append(i,params[i]);
    }

    xmlhttp.open("POST", "/approve_user", true);
    xmlhttp.onerror = function (e) {
        //alert('server error');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == 'ERROR'){
                btn.innerText(ans.message);
            } else {
                var host = location.host;
                location.href = "http://" + host + "/inprocess";
            }
        }
    };

    xmlhttp.send(formData);
}

function submitComment(user_id){
    var params = {};
    params['id'] = user_id;

    params['comment'] = document.getElementById('comment').value;

    var xmlhttp = getXHR();
    var formData = new FormData();
    for(var i in params){
        formData.append(i,params[i]);
    }

    xmlhttp.open("POST", "/comment_user", true);
    xmlhttp.onerror = function (e) {
        //alert('server error');
    };

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var ans = JSON.parse(xmlhttp.responseText);

            if (ans.status == 'ERROR'){
                btn.innerText(ans.message);
            } else {
                var host = location.host;
                location.href = "http://" + host + "/inprocess";
            }
        }
    };

    xmlhttp.send(formData);
}

function deleteRelative(but){
    but.parentElement.outerHTML = '';
}

function addFamilyMember(){
    count_relatives++;
    var members = document.getElementById('family-members');
    var member  = document.createElement('div');
    function make_input(header, cls, values){
        var starter = '<div class="input-group"><span class="input-group-addon">'+
                header + '</span>';
        var end = '<input class="form-control" class="family-' + cls + '" id = "' + cls + '"></div>'
        if (values){
            end = '<select class="form-control family-' + cls + '" id = "' + cls + '">';
            for (var i = 0; i < values.length; ++i){
                end += '<option>' + values[i] + '</option>';
            }
            end += '</select></div>';
        }
        return starter + end;
    }

    member.innerHTML = '<div class="well well-lg family-member">'+
        make_input('Кем приходится', 'who-' + String(count_relatives), ['Отец', 'Мать', 'Брат', 'Сестра', 'Сын', 'Дочь', 'Жена'])+
        make_input('Фамилия', 'last-name-' + count_relatives)+
            make_input('Имя', 'first-name-' + count_relatives)+
            make_input('Отчество', 'middle-name-' + count_relatives)+
            make_input('Мобильные телефоны', 'phones-' + count_relatives)+
            make_input('Фактический адрес', 'address-usual-' + count_relatives)+
            make_input('Адрес по прописке', 'address-registration-' + count_relatives)+
            '<button class="btn btn-danger ag-hor-center" type="button" onclick="deleteRelative(this);">Удалить</button>'+
        '</div><br>';
    members.appendChild(member);
}

function createAccounts(){
    var xmlhttp = getXHR();
    var file = document.getElementById('select-file').files[0];
    var vus = document.getElementById('vus').value;
    var btn = document.getElementById('status-btn');

    var formData = new FormData();
    formData.append('file', file);
    formData.append('vus', vus);

    xmlhttp.open("POST", "/create_accounts", true);
    xmlhttp.onerror = function (e) {
        btn.innerText('server error');
    };
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

            if (ans.status == 'ERROR'){
                btn.innerText(ans.message);
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

function checkAllElements(checkerId) {
    var i;
    var x = document.getElementById("checkbox-" + checkerId);
    x = x.getElementsByTagName('tr');
    var value = document.getElementById('checkall'+checkerId).checked;
    for (i = 1; i < x.length; i++) {
        x[i].childNodes[1].childNodes[0].checked=value;
    }
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
        label.getElementsByTagName('div')[0].innerText = 'OK';
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

function addUser(){
    var params = {
        login: document.getElementById('login').value,
        password: document.getElementById('password').value
    };
    var b = document.getElementById('create-but-1');

    complexXHR('/make_account', params,
        function(message, error){
            b.innerText = message;
        }, 0,
        function(ans){
            b.innerText = 'Создать аккаунт';
        }
    );
}


function postData(){
    //TODO: DO THIS!
}


///////////////////////////


function sleep (time) {
    return new Promise(function(resolve){setTimeout(resolve, time)});
}



