function showModal() {
	document.getElementById('detailModal').style.display='block';
}

function hideModal() {
	document.getElementById('detailModal').style.display='none';
}

<!-- JQUERY AJAX -->

        $(document).ready(function(){
            $("#cariData").click(function(e) {
				e.preventDefault();
				$.ajax({
                    url: 'http://127.0.0.1:5000/weather?city='+encodeURIComponent(document.getElementById('kota').value),
                    type:'GET',
                    dataType: 'json',
					crossDomain: true,
                    success: function(response) {
						console.log(response);
							document.getElementById('hasilkota').innerHTML = response['city'];
							document.getElementById('hasilnegara').innerHTML = response['country'];
							document.getElementById('lat').innerHTML = response['latitude'];
							document.getElementById('lon').innerHTML = response['longitude'];
							document.getElementById('main').innerHTML = response['main weather'];
							document.getElementById('desc').innerHTML = response['description'];
							document.getElementById('pressure').innerHTML = response['pressure'];
							document.getElementById('humidity').innerHTML = response['humidity'];
							document.getElementById('temp').innerHTML = response['temperature'];
							document.getElementById('wind').innerHTML = response['wind speed'];		
					},
					 error: function(response) {
                        console.log(response);
                    }
                });
				$.ajax({
                    url: 'http://127.0.0.1:5000/api/ytubesearch?keyword='+encodeURIComponent(document.getElementById('kota').value),
                    type:'GET',
                    dataType: 'json',
					contentType: 'application/json',
					crossDomain: true,
                    success: function(response) {
						console.log(response);
							content = '';
							var isivid = document.getElementById('tbodyvideo')
							$.each(response, function(key, value) {	
								content+=
								"<p>" +
									"<a>"+value.title+"</a>\n"+
									"<a><a href='"+value.url+"' target='_blank' >'"+value.url+"'</a>" +"</a>\n"+
								"</p><br/>";
							})
							isivid.innerHTML = content;
					},
					error : function(response) {
                        console.log(response);
                    }
                });
				// $.ajax({
       			// 	type : 'GET', 
				// 	url :"http://127.0.0.1:5000/api/youtubesearch?keyword="encodeURIComponent(document.getElementById('kota').value),
				// 	dataType : 'json',
				// 	crossDomain: true, 
				// 	contentType: 'application/json',
				// 	success : function(response) {
				// 		console.log(response);
				// 		content = '';
				// 		$.each(response, function(key, value) {
				// 			content+=
				// 				"<tr>" +
				// 					"<td>"+value.title+"</td>\n"+
				// 					"<td><a href='"+value.url+"' target='_blank' >links</a>" +"</td>\n"+
				// 				"</tr>";
				// 		});
				// 		tabmodiv.innerHTML = content;
				// 	}, 
				// 	error : function(response) {
				// 		console.log(response); 
				// 	}
				// });
		// 	}
		// }
			});
		});
