
function test() {
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/test", false );
    xmlHttp.send( null );
	var response = xmlHttp.responseText;
	response = JSON.parse(response);
	var iframe_div = document.createElement("div");
	iframe_div.style.height = "100%";
	iframe_div.style.width = "100%";
	iframe_div.style.visibility = "visible";
	var iframe_element = document.createElement("iframe");
	iframe_element.style.height = "100%";
	iframe_element.style.width = "100%";
	iframe_element.style.scrolling = "no";
	iframe_element.style.border = "none";
	iframe_element.id="iframe";
	
	iframe_div.appendChild(iframe_element);
	
	var getRef = document.getElementById("viewer");
	getRef.appendChild(iframe_div)
	
	var doc = document.getElementById('iframe').contentWindow.document;
	document.getElementById('loader').style.display = "None";
	
	for (var key in response) {
		if (response[key].main){
			doc.open();
			doc.write(response[key].data);
			doc.close();
		}
	}

	
	
}
document.onload = test();