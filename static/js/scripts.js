$(function(){
	$('button').click(function(){
		var name = $('#txtName').val();
		var phoneNumber = $('#txtPhoneNumber').val();
		$.ajax({
			url: '/register',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
