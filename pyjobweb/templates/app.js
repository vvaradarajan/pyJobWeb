var app = angular.module('angularjs-starter', [
  'charts.SBchart'
  ]); 



app.controller('MainCtrl', function($scope,$http) {
    /* Test data to be used when ajax is not working
     
     $scope.data = [
                ['Mushrooms', 3,5,2]
            ];
    */
     changeJsonObjectToDataArray($scope,$http);
     $scope.refresh = function(){
            changeJsonObjectToDataArray($scope,$http);
            };
           
    function changeJsonObjectToDataArray(scope,http) {
        http.get("http://localhost:5000/restful/jobs")
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
                        return angular.extend({ }, settings, scope.$eval(attr.qnPiechart));
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