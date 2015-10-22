
// Nav bar active setting
var cleanAll = function() {
	$("#homebutton").removeClass("active");
	$("#nodesbutton").removeClass("active");
	$("#containersbutton").removeClass("active");
};

$(document).ready(function() {
	$("#homebutton").click(function() {
		cleanAll();
		$("#homebutton").addClass("active");
	});

	$("#nodesbutton").click(function() {
		cleanAll();
		$("#nodesbutton").addClass("active");
	});

	$("#containersbutton").click(function() {
		cleanAll();
		$("#containersbutton").addClass("active");
	});
});


function postJson(url, data, callback) {
	$.ajax({
			url:url,
			type:"POST",
			data:data,
			contentType:"application/json; charset=utf-8",
			dataType:"json",
			success: callback
	});
}

angular.module('sensorship').controller('homeCtrl', function($scope) {

	$scope.submitTask = function() {
		try {
			var payload = $('#tasktext').val();
			var json = JSON.parse(payload);
		} catch (err) {
			alert("Invalid JSON: " + err);
			return;
		}

		postJson("/submit", payload, function(data) {
			console.log(data);
			$('#tasktext').val('');
			$scope.sync();
		});

	};

	$scope.sync = function() {
		$.getJSON("/tasks", function(data) {
			$scope.items = data;
			console.log($scope.items);
		});
	}

	$scope.toggle = function(id, state) {
		id = '{"id": "' + id + '"}';
		if (state == "on") {
			postJson("/off", id, function(data) {
				console.log(data)
				$scope.sync();
			});
		} else {
			postJson("/on", id, function(data) {
				console.log(data)
				$scope.sync();
			});
		}
	};

	$scope.sync();
});

angular.module('sensorship').controller('allNodesCtrl', function($scope) {
});

angular.module('sensorship').controller('nodeCtrl', function($scope) {
});

angular.module('sensorship').controller('containerCtrl', function($scope) {
});
