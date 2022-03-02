$("#top-search").on("keypress keyup blur",function (event) {
   $(this).val($(this).val().replace(/[^\d].+/, ""));
   if((event.which < 48 || event.which > 57)) event.preventDefault();
});

function search(){
  var value = $("#top-search").val();
  remove_valid("top-search");
  if(value.length >= 6){
    valid("top-search");
    location.href = '/request_page/CMS' + $('#top-search').val();
  } else {
    invalid("top-search");
  }
}

document.getElementById("top-search").addEventListener("keydown", function (e) {
  if (e.code === "Enter" || e.code == "NumpadEnter") search();
});
