window.onload = function () {
  console.log("Script loaded");
  //Load runs created
  function ucount() {
    fetch("/dcount?run=" + $("#runs").val() + "&field=" + $("#fields").val() )
      .then(res => res.json())
      .then(res => {
        let c = res["count"]
        $(".slider").attr("max", c)
      })
    $("#sinfo").html($(".slider").val() + "/" + $(".slider").attr("max"))
  }
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
      ucount()
  })
  $("#runs").on("change", function() {
    update()
    ucount()
    $("#slider").attr("value", "1")
  })
  $(".slider").on("change", function() {
    update()
    $("#sinfo").html($(".slider").val() + "/" + $(".slider").attr("max"))

  })
  $("#fields").on("change", function() {
    update()
    ucount()
    $("#slider").attr("value", "1")
  })
  setInterval(ucount, 5000)


}