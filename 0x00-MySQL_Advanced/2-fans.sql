-- SQL script that ranks country origins of bands,
-- ordered by the number of (non-unique) fans
select origin, COUNT(fans) AS nb_fans FROM metal_bands 
GROUP BY origin
HAVING nb_fans != 1 
ORDER BY nb_fans DESC;
