/**
 * 
 */

$(document).ready(function()
		{
	console.log("Entre AlBERTO BERNAL F")
	 const tiempo = Date.now();
	 	 alert(tiempo);
		document.getElementById("fecha").value = tiempo;

	  $('.table .eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			
			$.get(href, function(vistaCex,status)
					{
				$('.myForm #cita').val(vistaCex.cita);
				$('.myForm #fecha').val(vistaCex.fecha);
				$('.myForm #hora').val(vistaCex.hora);
				$('.myForm #consultorio').val(vistaCex.consultorio);
				$('.myForm #especialidad').val(vistaCex.especialidad);
				$('.myForm #medico').val(vistaCex.medico);
				$('.myForm #paciente').val(vistaCex.paciente);
				$('.myForm #estado_Cita').val(vistaCex.estado_Cita);
				
			
								
				if (vistaCex.llamada == true)
	               
					{
					
					$('.myForm #llamada').prop('checked',true);
						}
				else
					{
					
					$('.myForm #llamada').prop('checked',false);
					}
				
				
				if (vistaCex.atendido == true)
		               
				{
				
				$('.myForm #atendido').prop('checked',true);
					}
			else
				{
				
				$('.myForm #atendido').prop('checked',false);
				}
				
			})
			
		  
		  	$('.myForm #exampleModal').modal();
		  
			  });
	  
	})