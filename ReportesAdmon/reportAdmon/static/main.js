$(document).ready(function()
		{
		var envio = new FormData();
        alert("entre CArgue inicial");



	 $('.eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal x1");

			$.get(href, function(UsuariosHc,status)
			 {
			 alert("entre");


                $('#usuario').val(UsuariosHc.usuario);
				$('#contrasena').val(UsuariosHc.contrasena);
				$('#nombre').val(UsuariosHc.nombre);
				}
			);

			 $('#exampleModal').modal({show:true});

			  });


 $('.eBtn3').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre AlBERTO BERNAL F Cargue  Modal Contratos");

			$.get(href, function(UsuariosHc,status)
			 {
			 alert("entre modal contratos cuerpo");


                $('#usuario').val(UsuariosHc.usuario);

				$('#nombre').val(UsuariosHc.nombre);
				}
			);

			 $('#ModalContratos').modal({show:true});

			  });





		})

