$("#top-search").on("keypress keyup blur",function (event) {
   $(this).val($(this).val().replace(/[^\d].+/, ""));
   if((event.which < 48 || event.which > 57)) event.preventDefault();
});

function search(){
  var value = $("#top-search").val();
  remove_valid("top-search");
  if(value.length == 0){
    invalid("top-search");
  } else {
    valid("top-search");
    location.href = '/request_page/' + to_req_no(value);
  }
}

function to_req_no(value){
  var req_no = value.toString();
  while(req_no.length < 7){
    req_no = "0" + req_no;
  }
  req_no = "CMS" + req_no
  return req_no
}

document.getElementById("top-search").addEventListener("keydown", function (e) {
  if (e.code === "Enter" || e.code == "NumpadEnter") search();
});
