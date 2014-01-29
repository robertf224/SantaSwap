
var basePersonDiv = document.getElementById("person-base");
var personDiv = basePersonDiv.cloneNode();
basePersonDiv.parentNode.removeChild(basePersonDiv);
var personList = document.getElementById("person-list");

function next() {

	$('#screen1').fadeOut('fast', function() {
		$('#screen2').fadeIn('fast');
	});
}

function removePerson(person) {
	$(person).slideUp('fast', function() {
		personList.removeChild(person);
	});
}

function addPerson() {
	var person = personDiv.cloneNode();
	person.id = null;
	person.className = "person";
	personList.appendChild(person);
	$(person).show();
}

function back() {
	$('#screen2').fadeOut('fast', function() {
		$('#screen1').fadeIn('fast');
	});
}

function submit() {
	var groupName = $('input[name=group-name]')[0].value;
	var date = $('input[name=date]')[0].value;
	var limit = $('input[name=limit]')[0].value;

	var people = [];
	var personForms = $('.person form');
	for(var i = 0; i < personForms.length; i++) {
		if(personForms[i].name.value.length > 0 && personForms[i].email.value.length > 0) {
			people.push({'name': personForms[i].name.value, 'email': personForms[i].email.value});
		}
	}

	var requestData = {
		'group-name': groupName,
		'date': date,
		'limit': limit,
		'people': people
	};


	$('#screen2').fadeOut('fast', function() {
		$('#busy').fadeIn('fast', function() {
			$.ajax({
				url: '/',
				type: 'POST',
				data: JSON.stringify(requestData),
				contentType: 'application/json; charset=utf-8',
				success: function(data) {
					console.log('success');
					$('#busy').fadeOut('fast', function() {
						$('#screen3').fadeIn('fast');
					});
				},
				error: function(xhr, type) {
					console.log('error');
					console.log(type);
					$('#busy').fadeOut('fast', function() {
						$('#screen2').fadeIn('fast');
					});
				}
			});
		});
	});


}

