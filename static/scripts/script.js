window.onload = function () {
  console.log("Script loaded");
  //Load runs created
  function update() {
    $("#im").attr("src","/img?run=" + $("#runs").val() + "&field=" + $("#fields").val() + "&hour=" + $(".slider").val())
  }
  fetch("/dirs")
    .then(res => res.json())
    .then(res => {
      for (var item of res) {
        $("#runs").append(`
          <option value="${item}">${item}</option>
      `)
      $("#fields").css("display", "flex")
      }
      update()
  })
  $("#runs").on("change", update)
  $(".slider").on("change", update)
  $("#fields").on("change", update)


}