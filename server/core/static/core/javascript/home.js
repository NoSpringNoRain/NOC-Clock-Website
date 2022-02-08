$(document).ready(function(){
	$("#jobsform").submit(function() {
		$("#spinner").fadeIn();
	})
});

function showDiv(select){
	if(select.value==1){
		document.getElementById('hidden_diagnosis').style.display = "block";
	} else{
		document.getElementById('hidden_diagnosis').style.display = "none";
	}
}

function showOther(select){
	if(select.value==7){
		document.getElementById('hidden_other').style.display = "block";
	} else{
		document.getElementById('hidden_other').style.display = "none";
	}
}

function showCondition(select){
	if(select.value==1){
		document.getElementById('hidden_condition').style.display = "block";
	} else{
		document.getElementById('hidden_condition').style.display = "none";
	}
}

