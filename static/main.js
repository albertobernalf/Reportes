$(document).ready(function()
		{
		var envio = new FormData();

	console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal X0");
  alert("Active modal0");
	  $('.figure-img img-fluid rounded .eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
            alert("Active modal0");
			$.get(href, function(traslados,status)
			 {

                $('#usuario').val(traslados.usuario);
				$('#contrasena').val(traslados.contrasena);



					}
					
			);


			//	$('#exampleModal').modal("show");
				 $('#exampleModal').modal({show:true});

			  });

	// desde aqui

	 $('.table').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal x1");
            alert("Active modal1");
			$.get(href, function(UsuariosHC,status)
			 {
                 alert("Entre a cuerpo ...");
                $('#usuario').val(UsuariosHC.usuario);
				$('#contrasena').val(UsuariosHC.contrasena);
				$('#nombre').val(UsuariosHC.nombre);


					}

			);


			//	$('#exampleModal').modal("show");
				 $('#exampleModal1').modal({show:true});

			  });

	// hasta aqui


		})

