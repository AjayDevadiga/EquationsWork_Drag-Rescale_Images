
window.onload = () => {

  $("#ImageStream").hide();
  $("#sendbutton").click(() => {
  console.log("Analyse Button Clicked")
  $("#Stop").show()
  $("#sendbutton").hide()
  $("#ImageStream").show();
//  let formData = new FormData();
//          formData.append("Video", input.files[0]);
//          formData.append("InputType", "StartCamera");
//            $("#choosefileDiv").hide();
          $.ajax({
            url: "/CameraAction", // fix this to your liking
            type: "POST",
            data: "StartCamera",
            cache: false,
            processData: false,
            contentType: false,
            error: function (data) {
              console.log("upload error", data);
              console.log(data.getAllResponseHeaders());
            },
            success: function (data) {
              console.log(data);


              // bytestring = data["status"];
              // image = bytestring.split("'")[1];
//              $("#link").css("visibility", "visible");
//              $("#download").attr("href", "static/" + data);
//              console.log(data);
            },
          });
//    input = $("#imageinput")[0];
//    if (input.files && input.files[0]) {
//          let formData = new FormData();
//          formData.append("Video", input.files[0]);
//          formData.append("InputType", "Inputfile");
//            $("#choosefileDiv").hide();
//          $.ajax({
//            url: "/detect", // fix this to your liking
//            type: "POST",
//            data: formData,
//            cache: false,
//            processData: false,
//            contentType: false,
//            error: function (data) {
//              console.log("upload error", data);
//              console.log(data.getAllResponseHeaders());
//            },
//            success: function (data) {
//              console.log(data);
//
//              // bytestring = data["status"];
//              // image = bytestring.split("'")[1];
////              $("#link").css("visibility", "visible");
////              $("#download").attr("href", "static/" + data);
//              console.log(data);
//            },
//          });
//        }
  });

 $("#Stop").click(() => {
            $("#ImageStream").hide();
            let formData = new FormData();
            formData.append("InputType", "StopCamera");
//            window.location.reload();
            $.ajax({
            url: "/CameraAction", // fix this to your liking
            type: "POST",
            data: "StopCamera",
            cache: false,
            processData: false,
            contentType: false,
            error: function (data) {
              console.log("upload error", data);
              console.log(data.getAllResponseHeaders());
            },
            success: function (data) {
              console.log(data);
               $("#Stop").hide()
              $("#sendbutton").show()

              window.location.reload();

              // bytestring = data["status"];
              // image = bytestring.split("'")[1];
//              $("#link").css("visibility", "visible");
//              $("#download").attr("href", "static/" + data);
//              console.log(data);
            },
          });



  });

};
//function displayURLTextBox(){
// URLDIV = $('#URLTEXTDIV')
// DisplayDIV = $('#inputDIV')
//URLDIV.show();
//DisplayDIV.hide();
//Inputflag = "URLInput"
//
//}
//function displayInputBOX(){
// choosefileDiv = $('#choosefileDiv')
// DisplayDIV = $('#inputDIV')
//Inputflag = "FileInput"
//choosefileDiv.show();
//DisplayDIV.hide();
//
//}
//
//
////$('#rateToPost').on("change", function () {
////  alert($(this).val());
////});
//
//function displayAnalyseButton(){
//VIDEO_URL = $('#VIDEO_URL')
//console.log("Button CLicked")
//TextboxValue = VIDEO_URL.val()
//if(TextboxValue.startsWith("http"))
//{
//
//$('#sendbutton').show()
//
//}
//else
//{
//$('#sendbutton').hide()
//}
//
//}
//function readUrl(input) {
//  imagebox = $("#imagebox");
//  console.log(imagebox);
//  console.log("evoked readUrl");
//  if (input.files && input.files[0]) {
//    let reader = new FileReader();
//    reader.onload = function (e) {
//      console.log(e.target);
//      $('#sendbutton').show()
//
////      imagebox.attr("src", e.target.result);
//      //   imagebox.height(500);
//      //   imagebox.width(800);
//    };
//    reader.readAsDataURL(input.files[0]);
//  }
//  else{
//  $('#sendbutton').hide()
//  }
//}
//
//function changeValue(url){
//$('#VIDEO_URL').val(url);
//$('#sendbutton').show()
//}

