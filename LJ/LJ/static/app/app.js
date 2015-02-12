$(document).ready(function(){

// $('.ajax_call').click(function(e){
// 	e.preventDefault();
// 		alert("daa");
// 		// $.ajax({
// 		// 	url:'/add_comments',
// 		// 	type: 'POST',
// 		// 	data: $( "#form_comments" ).serialize(),
// 		// 	success:function(result) {

// 		// 	}

// 		// });
// 	});


	var max_fields      = 10; //maximum input boxes allowed

	var x = 1;
	$('#add_tags').click(function(e){
		e.preventDefault();
		 if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $('#append_tags').append('<div><input type="text" name="mytext"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
        }


	});

	$('#append_tags').on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    });

    // $('.show_comment').click(function(e){
    // 	e.preventDefault();
    // 	// $('#comment_div').html('<form action="." id="form_comments" method="post"><div><div><input type="text" name="user_name"/></div><div><textarea  name="user_comment"/><a class="ajax_call" onclick="ajax_call();">Submit</a></div></div><input type="hidden" name="csrf_token" value="django.middleware.csrf.get_token(request)"></form>');
    // 	//  $("#comment_div").load("../../LJblog/templates/LJblog/comment.html",function(){
    // 	// 	$(this).clone().appendTo("comment_div");
    // 	// });
    // $.ajax({
    //         url:'post/show_comments/',
    //         type: "GET",
    //         // dataType: 'html',   
    //         data: {'name': 'me', 'csrfmiddlewaretoken': '{{ csrf_token }}'},         
    //         success:function(result) {

    //         }

    //     });
    // 	$( this ).hide();
    // });

});

function blog_search(){
    var c_search      =   document.getElementById('blog_search').value;
    // c_search      =   document.getElementById('blog_search').value;
    // $.post('post/blog_search/', {blog_keyword: c_search}, function(data){
               
    //        });

       $.ajax({
            type: "POST",
            url:"post/blog_search/",
            data:{
                'search_text' : document.getElementById('blog_search').value,
                'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val() 
            },
            success: function(){
                alert("got");
            },
            dataType: 'html'

        });

}

