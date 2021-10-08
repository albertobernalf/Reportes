$(document).ready(function()
		{
		var envio = new FormData();

	console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal");
	alert ("Entre AlBERTO BERNAL F Cargue la Forma Modal");

	  $('.table .eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');

			$.get(href, function(vistaCex,status)
			 {


				$('#cita').val(vistaCex.cita1);
				$('#fecha').val(vistaCex.FECHA);
				$('#hora').val(vistaCex.HORA);
				$('#consultorio').val(vistaCex.CONSULTORIO);
				$('#especialidad').val(vistaCex.ESPECIALIDAD);
				$('#medico').val(vistaCex.MEDICO);
				$('#paciente').val(vistaCex.PACIENTE);
				$('.myForm #estado_Cita').val(vistaCex.ESTADO_CITA);

				if (vistaCex.LLAMADA == true)
	           		{
					
					$('#llamada').prop('checked',true);
						}
				else
					{
					
					$('#llamada').prop('checked',false);
					}
				
				
				if (vistaCex.ATENDIDO == true)
		               
				{
				
				$('#atendido').prop('checked',true);
					}
			else
				{
				
				$('#atendido').prop('checked',false);
				}
				

					}
					
			);

			//	$('#exampleModal').modal("show");
				 $('#exampleModal').modal({show:true});

			  });

		})

