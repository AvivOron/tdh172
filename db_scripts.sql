select * from poets
select count(*) from poems where poet_id > 50
select * from poems where poet_id = 79

/*delete from poems where id > 0;
delete from poets where id > 0;*/

select p.name as 'Poem name', pt.name as 'Poet name' , p.original_data, p.translated_data from poems p join poets pt on p.poet_id = pt.id limit 20
