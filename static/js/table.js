function mysortTable(column) {
var tables, rows, sorting, c, a, b, tblsort;
tables = document.getElementById("sortingTable");
sorting = true;
while (sorting) {
sorting = false;
rows = tables.rows;
for (c = 1; c < (rows.length - 1); c++) {
tblsort = false;
a = rows[c].getElementsByTagName("TD")[column];
b = rows[c + 1].getElementsByTagName("TD")[column];
if (a.innerHTML.toLowerCase() > b.innerHTML.toLowerCase()) {
tblsort = true;
break;
}
}
if (tblsort) {
rows[c].parentNode.insertBefore(rows[c + 1], rows[c]);
sorting = true;
}
}
}
