
$(document).ready( function () {
	syncNotifications();
});
setInterval(function(){
	syncNotifications();

}, 5000);



const spinner = '<i class="fa fa-spinner fa-pulse fa-4x fa-fw"></i><span class="sr-only">Loading...</span>'
function markRead(id) {
	document.getElementById('noti_table_div').innerHTML = spinner;
	let data = new FormData();
	data.append('id', id);
	const url = "/janta/mark-as-read/";
	const req = new XMLHttpRequest();
	req.open("POST",url,true);
	req.send(data);
	req.onreadystatechange=function(){
		if (req.readyState === 4 && req.status === 200) {
			const result = req.responseText;
			const response = JSON.parse(result);
			const status = response["Status"];
			if(status === 1) {
				syncNotifications();
			}
		}
	};
}

function syncNotifications(){
	const url = "/janta/get-notifications/";
	const req = new XMLHttpRequest();
	req.open("POST",url,true);
	req.send(null);
	req.onreadystatechange=function(){
		if (req.readyState === 4 && req.status === 200) {
			const result = req.responseText;
			const response = JSON.parse(result);
			const count = response["Count"];
			const unread_count = response['UnreadCount']

			if (count > 0) {
				const data = response["Data"]

				// construct notification count
				let noti_html = '<span><i class="fa fa-bell fa-lg"></i><sup><span id="unread_count" class="badge badge-danger">'+unread_count+'</span></sup>' +
					' <b>Notifications</b></span><br><br>'
				if(unread_count === 0) {
					noti_html = '<span><i class="fa fa-bell fa-lg"></i> <b>Notifications</b></span><br><br>'
				}

				// construct table.
				noti_html += "<div id='noti_table_div'><table>";
				for (let i = 0; i < count; i++) {
					noti_html += '<tr style="text-align:left; border: 2px solid white;"><td>';
					if (data[i].marked === 0) {
						noti_html += '<button class="btn btn-success btn-sm float-right" onclick=markRead('+data[i].id+');>' +
							'<i class="fa fa-check" aria-hidden="true"></i></button>';
					}
					noti_html += data[i].text;
					noti_html += " on "+data[i].noti_time;
					noti_html += "</td></tr>";
				}
				noti_html += "</table></div>";

				document.getElementById('notification_div').innerHTML = noti_html;
			} else {
				let noti_html = '<span><i class="fa fa-bell fa-lg"></i>&nbsp; <b>Notifications</b></span><br><br>'
				document.getElementById('notification_div').innerHTML = noti_html+"No notifications";
			}
		}
	};
}
