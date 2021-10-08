$(document).ready(function()
		{
		var envio = new FormData();

	console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal X");

	  $('.table .eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');

			$.get(href, function(vistaCex,status)
			 {

                $('#cita').val(vistaCex.cita1);
				$('#fecha').val(vistaCex.fecha);
				$('#hora').val(vistaCex.hora);
				$('#consultorio').val(vistaCex.consultorio);
				$('#especialidad').val(vistaCex.especialidad);
				$('#medico').val(vistaCex.medico);
				$('#paciente').val(vistaCex.paciente);
				$('.myForm #estado_Cita').val(vistaCex.estado_cita);



				if (vistaCex.llamada == true)
	           		{
					
					$('#llamada').prop('checked',true);
						}
				else
					{
					
					$('#llamada').prop('checked',false);
					}
				



				if (vistaCex.atendido == true)
		               
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

