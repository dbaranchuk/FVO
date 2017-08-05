select u_id, u_role, u_login, bi_last_name,
VUS.number as 'vus_num',
VUS.code as 'vus_code'
from (
select user.id as 'u_id',
user.role as 'u_role',
user.login as 'u_login',
user.vus_id as 'u_vus_id',
bi_last_name
from (
select
student_info.user_id as 'si_user_id',
basic_information.last_name as 'bi_last_name'
from student_info left join basic_information
on student_info.id = basic_information.student_info_id) as X
left join user
on X.si_user_id = user.id) as Y
left join VUS
on Y.u_vus_id = VUS.id