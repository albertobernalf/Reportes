$(document).ready(function()
		{
		var envio = new FormData();

	console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal X");

	  $('.table .eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');

			$.get(href, function(Traslados,status)
			 {

                $('#mpdisp').val(Traslados.MPDISP);
				$('#mpnumc').val(Traslados.MPNUMC);
				$('#mpudoc').val(Traslados.MPUDOC);
				$('#mpuced').val(Traslados.MPUCED);
				$('#mpnomc').val(Traslados.MPNOMC);
				$('#mpfchi').val(Traslados.MPFCHI);
				$('#estancia').val(Traslados.ESTANCIA);
				$('#mpcodp').val(Traslados.MPCODP);
				$('.myForm #observaciones').val(Traslados.OBSERVACIONES);



				




				

					}
					
			);


			//	$('#exampleModal').modal("show");
				 $('#exampleModal').modal({show:true});

			  });

		})

