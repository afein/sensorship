
// Nav bar underlining of clicked links
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


angular.module('sensorship').controller('homeCtrl', function($scope) {
});

angular.module('sensorship').controller('allNodesCtrl', function($scope) {
});

angular.module('sensorship').controller('nodeCtrl', function($scope) {
});

angular.module('sensorship').controller('containerCtrl', function($scope) {
});
