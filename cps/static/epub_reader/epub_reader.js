
var file_name = null;
//var iframe = null;
var response = null;


function add_style(){
	var id ="inserted_css";
	var iframe = document.getElementById('iframe');
	var style_element = document.getElementById('iframe').contentWindow.document.getElementById(id);
	
	style_element = document.getElementById('iframe').contentWindow.document.createElement("style");
	style_element.id=id;

	document.getElementById('iframe').contentWindow.document.head.appendChild(style_element);
	
	var style_sheet =  style_element.sheet;
	var height = parseInt(iframe.style.height,10);
	var width = document.getElementById("viewer").clientWidth;
	var str = "img { object-fit: contain; break-inside: avoid; max-height: "+height*0.9+"px !important; max-width: "+width*0.9+"px !important }";
	style_sheet.insertRule(str,0);
}


function create_iframe(){
	var container_div = document.createElement("div");
//	container_div.style.wordSpacing = "0px";
//	container_div.style.lineHeight = "0";
//	container_div.style.verticalAlign = "top";
//	container_div.style.position = "relative";
	container_div.style.width = "100%";
	container_div.style.height = "100%";
	//container_div.style.overflow = "hidden";
//	container_div.style.direction = "ltr";
//	container_div.style.display = "flex";
//	container_div.style.flexFlow = "column nowrap";
	container_div.id = "container_div";
	
	var iframe_div = document.createElement("div");
	var client_height = document.getElementById("viewer")
	client_height = client_height.clientHeight;
	//iframe_div.style.height = document.getElementById("viewer").scrollHeight+"px";
	iframe_div.style.width = "100%";
//	iframe_div.style.width = document.getElementById("viewer").clientWidth+"px";
//	iframe_div.style.visibility = "visible";
	//iframe_div.style.overflow = "hidden";
//	iframe_div.style.position = "relative";
//	iframe_div.style.display = "block";
//	iframe_div.style.flex = "0 0 auto";
	iframe_div.id = "iframe_div";
    iframe_div.style.height = "100%";
	
	var iframe_element = document.createElement("iframe");
	iframe_element.style.height = "100%";
	iframe_element.style.width = "100%";
//	iframe_element.style.width = document.getElementById("viewer").clientWidth+"px";
	//iframe_element.style.overflow = "hidden";
	//iframe_element.style.scrolling = "no";
//	iframe_element.style.border = "none";
//	iframe_element.style.visibility = "visible";
	iframe_element.id="iframe";
	//iframe_element.scrolling="no";
	iframe = iframe_element;
	//iframe_element.style.height = "750px";
	
	container_div.appendChild(iframe_div);
	iframe_div.appendChild(iframe_element);

	
	var getRef = document.getElementById("viewer");
	getRef.appendChild(container_div);
}



function fill_iframe(data){
	var doc = document.getElementById('iframe').contentWindow.document;
	document.getElementById('loader').style.display = "None";	
	doc.open();
	doc.write(data);
	doc.close();
	add_style();
	//var iframe = document.getElementById('iframe');
	//iframe.srcdoc = data;
	var viewer = document.getElementById("viewer")
	client_height = viewer.clientHeight;
	var client_width = viewer.clientWidth;
	
	//doc.body.style.margin = "0px !important";
//	doc.body.style.cssText = "margin: 0px !important; padding: 20px !important";
	//doc.body.style.padding = "20px !important";
	//doc.body.style.overflowY = "hidden";
//	doc.body.style.boxSizing = "border-box";
//	doc.body.style.maxWidth = "inherit";
	//doc.body.style.columnFill = "auto";
	//doc.body.style.height = "100%";
//	doc.body.style.width = client_width+"px";
	//doc.body.style.columnWidth = client_width+"px";
//	doc.body.style.columnGap = "40px";
	
	//var iframe_div = document.getElementById("iframe_div")
	var iframe_doc = document.getElementById('iframe').contentWindow.document;
	var test = iframe_doc.body.offsetHeight;
//	var height = Math.max(iframe_doc.body.scrollHeight, iframe_doc.body.offsetHeight, 
//						  iframe_doc.documentElement.clientHeight, iframe_doc.documentElement.scrollHeight,
//						  iframe_doc.documentElement.offsetHeight)+"px";
//	document.getElementById("container_div").style.height = "100%";
//	document.getElementById("iframe_div").style.height = height;
//	document.getElementById("iframe").style.height = height;
	
}

var head_add_cnt = 0;

function extract_and_add_elements(main_page){
	document.getElementById('loader').style.display = "block";
	document.getElementById('loader').style.display = "None";
	var head = document.head;
	while  (head_add_cnt > 0){
		head.removeChild(head.lastElementChild);
		head_add_cnt--;
	}
	
	var viewer = document.getElementById('viewer');
	var child = viewer.lastChild;
	while (child) { 
            viewer.removeChild(child); 
            child = viewer.lastElementChild; 
    } 
	var el = document.createElement( 'html' );
	el.innerHTML = main_page.trim();
	var tmp_head = el.getElementsByTagName('head')[0];
	head_add_cnt = 0;
	for (var i = 0; tmp_head.childNodes.length;i++){
		if (tmp_head.childNodes[i].nodeName != '#text'){
			head.appendChild(tmp_head.childNodes[i]);
			head_add_cnt++;
		}
	}
		
	var tmp_body = el.getElementsByTagName('body')[0];
	for (var i =0; i < tmp_body.childNodes.length; i++){
		viewer.appendChild(tmp_body.childNodes[i]);
	}
	
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
				var blob =new Blob([response[key].data],{type: "text/css"});
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
		//fill_iframe(main_page);
		extract_and_add_elements(main_page);
	}
    xmlHttp.send( null );
}

function load_file(URL){
	get_data(URL);
}

function onload_routine() {
	//create_iframe();
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB"
	load_file(URL);	
}
function next(){
	//var client_width = document.getElementById('iframe').contentWindow.document.body.clientWidth;
	//client_height = client_height.clientHeight;
	//var doc = document.getElementById('iframe').contentWindow.document;
	//var scroll_left = doc.body.scrollLeft;
	//var scroll_width = doc.body.scrollWidth;
	//if (scroll_left + client_width < scroll_width){
	//	doc.body.scrollBy(client_width,0);
	//} else {
	//	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isNext=True";
	//	load_file(URL);	
	//}
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isNext=True";
		load_file(URL);	
}

function previous(){
	//var client_height = document.getElementById('iframe_div')
	//client_height = client_height.clientHeight;
	//var doc = document.getElementById('iframe').contentWindow.document;
	//var scroll_top = doc.body.scrollTop;
	////var scroll_height = doc.body.scrollHeight;
	//if (scroll_top>0){
	//	doc.body.scrollBy(0,-client_height);
	//} else {
	//	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isPrevious=True";
	//	load_file(URL);	
	//}
	var URL = "/api/books/"+window.calibre.book_id+"?bookFormat=EPUB&fileName="+file_name+"&isPrevious=True";
		load_file(URL);
}



function addListeners(){
	var right_arrow = document.getElementById("next");
	right_arrow.addEventListener("click", next);
	var left_arrow = document.getElementById("prev");
	left_arrow.addEventListener("click", previous);
	//document.getElementById('iframe').addEventListener("load",function () {
	//	var height = document.getElementById('iframe').contentWindow.document.body.scrollHeight;
//		document.getElementById("iframe_div").style.height = height+"px";
//		document.getElementById('iframe').style.height = height+"px";
//		document.getElementById("container_div").style.height = height+"px";
	//	document.getElementById("viewer").style.height = "100%";
	//	document.body.style.height = height+"px";
	//});
}
document.onload = onload_routine();
addListeners();