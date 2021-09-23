function switchFeed(id) {
  console.log(id)
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", "http://127.0.0.1:5000/switch_feed?camera=" + id, false ); // false for synchronous request
  xmlHttp.send( null );
  console.log(xmlHttp.status == 200)
  console.log(xmlHttp.status)
  if (xmlHttp.status == 200){
    document.getElementById("feed").src = "http://127.0.0.1:5000/video_feed?camera=" + id;
  }  
}
