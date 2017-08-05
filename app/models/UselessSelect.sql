WITH Y as (
select *
FROM 
(
select student_info.user_id AS 'user_id', student_info.id AS 'id'
from (student_info
left join basic_information
on student_info.id = basic_information.student_info_id)
where last_name = 'Сташевский' ) AS X
LEFT JOIN 
user
on user.id = X.user_id
where (user.role = 0) 
AND (user.login like '%2016')
)
select Y.user_id
from Y
left join VUS
ON Y.vus_id = VUS.id
WHERE number = '188';