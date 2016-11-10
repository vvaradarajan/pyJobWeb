/* A self stopping time Global function:
 * g_v = global timer (obtained from gb
 * g_refresh => calls g_v refresh with g_v as this
 * g_reset => call g_v reset with g_v as this
 * objectFcnNM => function to be called at each timer interval
 */
function gb(objectFcnNM,interval) {
	
	return {
		noOfSamples: 20,
		CnoOfSamples:0,
		timerOn: true,
		timerInterval: 1000,
		objectFcnNM:objectFcnNM,
		timerId:null,
		interval: interval,
		refresh: function() {
			this.CnoOfSamples --;
			if (this.CnoOfSamples > 0)  this.objectFcnNM();
			else this.stop();
		},
		reset: function() {
			this.CnoOfSamples=this.noOfSamples;
			this.timerOn=true;
			this.timerId = this.interval(g_refresh,this.timerInterval,this.noOfSamples)
		},
		stop: function() {
			this.timerOn=false;
			interval.cancel(this.timerId);
		}
	}
}

function g_refresh() {
	g_v.refresh.call(g_v);
}
function g_timeReset() {
	g_v.reset.call(g_v);
}
var g_v=null;

var app = angular.module('angularjs-starter', [
  'charts.SBchart'
  ]); 

/* chartCtrl is for google chart*/
myChartCtrl = app.controller('chartCtrl', function($scope,$http,$interval) {
    /* Test data to be used when ajax is not working
     
     $scope.data = [
                ['Mushrooms', 3,5,2]
            ];
    */
    changeJsonObjectToDataArray($scope,$http);
    $scope.refresh = function(){
            changeJsonObjectToDataArray($scope,$http);
            };
    /*initialize the global object for timer*/
    g_v=gb($scope.refresh,$interval);
     
    function changeJsonObjectToDataArray(scope,http) {
        http.get("/restful/Status")
        .then(function(response) {
        	console.log(response.data)
            updateChartWithResponse(scope,response.data)
        });
    }

    function updateChartWithResponse(scope,Jo) {
      /*
       * The format of the ajax response from server : 1st two rows indicate the column meta data (label and type)
       * After that are the data rows
       * ex: [["jobId", "idle", "executing", "complete"], ["string", "number", "number", "number"], ["a", 1103, 1001, 20], ["b", 1109, 5000, 20], ["c", 6119, 6001, 20], ["d", 0, 997, 20], ["e", 9, 1001, 20], ["f", 1001, 1002, 20]]
       */
      var arrayLength = Jo.length;
      var jobs=Jo;
      var s=[]
      //push the column data in 1st two rows
      scope.data=Jo;
      scope.name="Gazebo"
    }
    $scope.echo = function () {
    	alert("From chartCtrl - echo");
    }
});

angular.module('charts.SBchart', [
])
    .directive('qnSbchart', [
        function() {
            return {
                require: '?ngModel',
                link: function(scope, element, attr, controller) {
                    var settings = {
                        is3D: true,
                        isStacked:true
                    };
                    var getOptions = function() {
                        return angular.extend({ }, settings, scope.$eval(attr.qnSbchart));
                    };

                    // creates instance of datatable and adds columns from settings
                    var getDataTable = function() {
                        var columns = scope.$eval(attr.qnColumns);
                        var data = new google.visualization.DataTable();
                        console.log(data);
                        return data;
                    };

                    var init = function() {
                        var options = getOptions();
                        console.log("Data changed");
                        if (controller) {

                            var drawChart = function() {
                                var data = getDataTable();
                                if (controller.$viewValue == undefined) {console.log("dataValue undefined"); return;};
                                console.log(controller.$viewValue);
                                var rows=controller.$viewValue;
                                colNames=rows[0];colTypes=rows[1];
                                for (var i=0; i < colNames.length; i++) {
                                	console.log(colNames[i] + " is "+colTypes[i]);
                                	data.addColumn(colTypes[i],colNames[i]);
                                }
                                // set model
                                
                                for(var i = 2; i < rows.length; i++) 
                                	data.addRow(rows[i]);
                                // Instantiate and draw our chart, passing in some options.
                                var pie = new google.visualization.ColumnChart(element[0]);
                                pie.draw(data, options);
                            };

                            controller.$render = function() {
                                drawChart();
                            };
                        }

                        if (controller) {
                            // Force a render to override
                            console.log("Rendering");
                            controller.$render();
                        }
                    };

                    // Watch for changes to the directives options
                    scope.$watch(getOptions, init, true);

                }
            };
        }
    ]);

/* main Ctrl for displaying table below chart*/
app.controller('mainCtrl', function($scope,$http) {
	$scope.StartJobs = function() {
		//ajax call to start jobs of a jobset and also return the lineal time
		$http.get("/restful/StartJobs/ProjectG")
        .then(function(response) {
        	console.log(response.data)
        	g_v.noOfSamples=response.data.linealTime;
            g_timeReset.call(g_v);
        });
	};
	$http.get("/restful/JobList/ProjectG")
	  .then (function(response){
		  cb_popJobData($scope,response.data)
	  })
	function cb_popJobData(scope,jobArray) {
		/* create a heading from the 1st row */
		scope.RowTitles=jobArray[0];
		jobArray.splice(0,1)
		scope.jobArray=jobArray;
		scope.TableTitle="Job List";
	}
});
