
var file_name = null;
//var iframe = null;
var response = null;



function create_iframe(){
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
	iframe = iframe_element;
	
	iframe_div.appendChild(iframe_element);
	
	var getRef = document.getElementById("viewer");
	getRef.appendChild(iframe_div);
}



function fill_iframe(data){
	var doc = document.getElementById('iframe').contentWindow.document;
	document.getElementById('loader').style.display = "None";
	doc.open();
	doc.write(data);
	doc.close();
}

function get_main_page(response){
	var main_page = null;
	for (var key in response) {
		if (response[key].main){
			main_page = response[key].data;
			file_name = key
		}
	}
	return main_page;
}

function get_blobs(response){
	var data = {};
	for (var key in response) {
		if (!response[key].main){
			if (response[key].type==="STYLE"){
				var blob =new Blob([response[key].data],{type: "text/plain"});
				var blob_url = window.URL.createObjectURL(blob);
				var content = {};
				content["url"] = blob_url;
				content["type"] = response[key].type;
				data[key] = content;
			}
			else if (response[key].type==="IMAGE"){
				const byteCharacters = atob(response[key].data);
				const byteNumbers = new Array(byteCharacters.length);
				for (let i = 0; i < byteCharacters.length; i++) {
					byteNumbers[i] = byteCharacters.charCodeAt(i);
				}
				const byteArray = new Uint8Array(byteNumbers);
				const blob = new Blob([byteArray], {type: "image/*"});
				var blob_url = window.URL.createObjectURL(blob);
				var content = {};
				content["url"] = blob_url;
				content["type"] = response[key].type;
				data[key] = content;
			}
		}
	}
	return data;
}

function replace_with_blobs(main_page, blobs){
	
	for (var key in blobs){
		if (blobs[key].type === "STYLE"){
			var re = new RegExp('(<link.*href=")'+key+'(")');
			main_page = main_page.replace(re,'$1'+blobs[key].url+'$2');
		} else if (blobs[key].type === "IMAGE"){
			var re = new RegExp('(<img.*src=")'+key+'(")');
			main_page = main_page.replace(re,'$1'+blobs[key].url+'$2');
		}
	}
	return main_page;
}

function prepare_page(response){
	var main_page = get_main_page(response);
	var blobs = get_blobs(response);
	main_page = replace_with_blobs(main_page,blobs);
	return main_page;
}


function get_data(address){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", address, true );
	xmlHttp.onreadystatechange = function(){
		if (xmlHttp.readyState !=4) return;
		
		response = xmlHttp.responseText;
		response = JSON.parse(response);	
		var main_page = prepare_page(response);
		fill_iframe(main_page);
	}
    xmlHttp.send( null );
}

function load_file(URL){
	get_data(URL);
}

function load_next_file(){
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isNext=True";
	load_file(URL);		
}

function load_previous_file(){
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isPrevious=True";
	load_file(URL);		
}

function addListeners(){
	var right_arrow = document.getElementById("next");
	right_arrow.addEventListener("click", load_next_file);
	var left_arrow = document.getElementById("prev");
	left_arrow.addEventListener("click", load_previous_file);
}
document.onload = function(){
	create_iframe();
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB"
	load_file(URL);
};
addListeners()