angular.module("getbookmarks.services", ["ngResource"]).
    factory('Story', function ($resource) {
        var Story = $resource('/api/v1/stories/:storyId', {storyId: '@id'});
        var Comment = $resource('/index', {});
        var Like = $resource('/like/:storyId', {storyId: '@id'});
        Story.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return {
        Comments : Comment,
        Storys : Story,
        Likes : Like,
        };
    });

// angular.module(name, [requires], [configFn]);
// requires - If specified then new module is being created. If unspecified then the module is being retrieved for further configuration.
// (optional)
  
angular.module("getbookmarks", ["getbookmarks.services"]).
    config(function ($routeProvider) {
        $routeProvider
            .when('/', {templateUrl: '/static/views/stories/list.html', controller: StoryListController})
            .when('/stories/new', {templateUrl: '/static/views/stories/create.html', controller: StoryCreateController})
            .when('/stories/:storyId', {templateUrl: '/static/views/stories/detail.html', controller: StoryDetailController})
            .when('/like/:storyId', {templateUrl: '/static/views/stories/list.html', controller: StoryLikeController});
    });

function StoryLikeController($scope, $routeParams, $location, Story)
{
    var storyId = $routeParams.storyId;
    
    $scope.story = Story.Likes.get({storyId: storyId});

   $location.path('/');

     
}

function StoryListController($scope, Story) {
    // We can retrieve a collection from the server
    $scope.stories = Story.Storys.query();

   
    
}

function StoryCreateController($scope, $routeParams, $location, Story) {

    $scope.story = new Story.Storys();

    // $scope.story = {};
    $scope.items = [];
    $scope.story.tag = $scope.items;

    $scope.save = function () {
        // headers => $http header getter
        //  The actions save, remove and delete are available on it as methods with the $ prefix.
        console.log($scope.story);

    	$scope.story.$save(function (story, headers) {
    		toastr.success("Submitted New Story");
            $location.path('/');
        });
    };

    $scope.add = function () {
        $scope.items.push({
            tag: "",
        });
        console.log($scope.story);
    };
}


function StoryDetailController($scope, $routeParams, $location, Story) {
    var storyId = $routeParams.storyId;
    
    $scope.story = Story.Storys.get({storyId: storyId});

    $scope.comment = new Story.Storys();

     $scope.save_comment = function () {
        // headers => $http header getter
        //  The actions save, remove and delete are available on it as methods with the $ prefix.
        console.log($scope.comment);
        $scope.comment.post_id = $scope.story._id.$oid
        $scope.comment.$save(function (story, headers) {
            toastr.success("Submitted Your Comments");
            $location.path('/');
        });
    };


}

$("button").on("click", function () {
    var state = $(this).data('state');
    state = !state;
    if (state) {
        $("span").addClass("show");
    } else {
        $("span").removeClass("show");
    }
    $(this).data('state', state);
});



function search(){
     $.ajax({
            type: "POST",
            url:"/search",
            data:{
                'search_text' : document.getElementById('search').value,
            },
            success: function(data){
               $('#manage_user table > tbody:first').append(data);
            },
            
        });
}
