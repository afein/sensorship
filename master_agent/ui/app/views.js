
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


angular.module('sensorship').controller('homeCtrl', function($scope, $http) {

	$scope.submitTask = function() {
		try {
			var payload = $('#tasktext').val();
			var json = JSON.parse(payload);
		} catch (err) {
			alert("Invalid JSON: " + err);
			return;
		}

		var res = $http.post("/submit", payload)
		res.success(function(data, status, headers, config) {
			console.log("done");
			$('#tasktext').val('');
			$scope.sync(true);
		});

	};

	$scope.sync = function(apply) {
		$.getJSON("/tasks", function(data) {
			if (apply) {
				$scope.$apply(function() {
					$scope.items = data;
				});
			} else {
				$scope.items = data;
			}
			console.log($scope.items);
		});
	}

	$scope.toggle = function(id, state) {
		id = '{"id": "' + id + '"}';
		if (state == "on") {
			var res = $http.post("/off", id);
			res.success(function(data, status, headers, config) {
				$scope.sync(true);
			});
		} else {
			var res = $http.post("/on", id);
			res.success(function(data, status, headers, config) {
				$scope.sync(true);
			});
		}
	};

	$scope.sync(false);
});

angular.module('sensorship').controller('allNodesCtrl', function($scope) {
});

angular.module('sensorship').controller('nodeCtrl', function($scope) {
});

angular.module('sensorship').controller('containerCtrl', function($scope) {
});
