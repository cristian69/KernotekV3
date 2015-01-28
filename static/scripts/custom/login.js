var Login = function () {

	/**
	 * Description
	 * @method handleLogin
	 * @return 
	 */
	var handleLogin = function() {

		$('.login-form').validate({
	            errorElement: 'span', //default input error message container
	            errorClass: 'help-block', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            rules: {
	                username: {
	                    required: true
	                },
	                password: {
	                    required: true
	                },
	                remember: {
	                    required: false
	                }
	            },

	            messages: {
	                username: {
	                    required: "Nombre de usuario requerido"
	                },
	                password: {
	                    required: "Password requerido."
	                }
	            },

	            /**
            	 * Description
            	 * @method invalidHandler
            	 * @param {} event
            	 * @param {} validator
            	 * @return 
            	 */
            	invalidHandler: function (event, validator) { //display error alert on form submit   
	                $('', $('.login-form')).show();
	            },

	            /**
            	 * Description
            	 * @method highlight
            	 * @param {} element
            	 * @return 
            	 */
            	highlight: function (element) { // hightlight error inputs
	                $(element)
	                    .closest('.form-group').addClass('has-error'); // set error class to the control group
	            },

	            /**
            	 * Description
            	 * @method success
            	 * @param {} label
            	 * @return 
            	 */
            	success: function (label) {
	                label.closest('.form-group').removeClass('has-error');
	                label.remove();
	            },

	            /**
            	 * Description
            	 * @method errorPlacement
            	 * @param {} error
            	 * @param {} element
            	 * @return 
            	 */
            	errorPlacement: function (error, element) {
	                error.insertAfter(element.closest('.input-icon'));
	            },

	            /**
            	 * Description
            	 * @method submitHandler
            	 * @param {} form
            	 * @return 
            	 */
            	submitHandler: function (form) {
	                form.submit(); // form validation success, call ajax form submit
	            }
	        });

	        $('.login-form input').keypress(function (e) {
	            if (e.which == 13) {
	                if ($('.login-form').validate().form()) {
	                    $('.login-form').submit(); //form validation success, call ajax form submit
	                }
	                return false;
	            }
	        });
	}

	/**
	 * Description
	 * @method handleForgetPassword
	 * @return 
	 */
	var handleForgetPassword = function () {
		$('.forget-form').validate({
	            errorElement: 'span', //default input error message container
	            errorClass: 'help-block', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            ignore: "",
	            rules: {
	                email: {
	                    required: true,
	                    email: true
	                }
	            },

	            messages: {
	                email: {
	                    required: "Email requerido."
	                }
	            },

	            /**
            	 * Description
            	 * @method invalidHandler
            	 * @param {} event
            	 * @param {} validator
            	 * @return 
            	 */
            	invalidHandler: function (event, validator) { //display error alert on form submit   

	            },

	            /**
            	 * Description
            	 * @method highlight
            	 * @param {} element
            	 * @return 
            	 */
            	highlight: function (element) { // hightlight error inputs
	                $(element)
	                    .closest('.form-group').addClass('has-error'); // set error class to the control group
	            },

	            /**
            	 * Description
            	 * @method success
            	 * @param {} label
            	 * @return 
            	 */
            	success: function (label) {
	                label.closest('.form-group').removeClass('has-error');
	                label.remove();
	            },

	            /**
            	 * Description
            	 * @method errorPlacement
            	 * @param {} error
            	 * @param {} element
            	 * @return 
            	 */
            	errorPlacement: function (error, element) {
	                error.insertAfter(element.closest('.input-icon'));
	            },

	            /**
            	 * Description
            	 * @method submitHandler
            	 * @param {} form
            	 * @return 
            	 */
            	submitHandler: function (form) {
	                form.submit();
	            }
	        });

	        $('.forget-form input').keypress(function (e) {
	            if (e.which == 13) {
	                if ($('.forget-form').validate().form()) {
	                    $('.forget-form').submit();
	                }
	                return false;
	            }
	        });

	        jQuery('#forget-password').click(function () {
	            jQuery('.login-form').hide();
	            jQuery('.forget-form').show();
	        });

	        jQuery('#back-btn').click(function () {
	            jQuery('.login-form').show();
	            jQuery('.forget-form').hide();
	        });

	}

	/**
	 * Description
	 * @method handleRegister
	 * @return 
	 */
	var handleRegister = function () {

		/**
		 * Description
		 * @method format
		 * @param {} state
		 * @return BinaryExpression
		 */
		function format(state) {
            if (!state.id) return state.text; // optgroup
            return "<img class='flag' src='../static/img/flags/normal.png'/>&nbsp;&nbsp;" + state.text;
        }


		$("#tipo_cuenta").select2({
		  	placeholder: '<i class="fa fa-user"></i>&nbsp;Tipo de cuenta',
            allowClear: true,
            formatResult: format,
            formatSelection: format,
            /**
             * Description
             * @method escapeMarkup
             * @param {} m
             * @return m
             */
            escapeMarkup: function (m) {
                return m;
            }
        });


			$('#select2_sample4').change(function () {
                $('.register-form').validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
            });



         $('.register-form').validate({
	            errorElement: 'span', //default input error message container
	            errorClass: 'help-block', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            ignore: "",
	            rules: {
	                
	                fullname: {
	                    required: true
	                },
	                email: {
	                    required: true,
	                    email: true
	                },
	                address: {
	                    required: true
	                },
	                city: {
	                    required: true
	                },
	                country: {
	                    required: true
	                },

	                username: {
	                    required: true
	                },
	                password: {
	                    required: true
	                },
	                rpassword: {
	                    equalTo: "#register_password"
	                },

	                tnc: {
	                    required: true
	                }
	            },

	            messages: { // custom messages for radio buttons and checkboxes
	                tnc: {
	                    required: "Please accept TNC first."
	                }
	            },

	            /**
            	 * Description
            	 * @method invalidHandler
            	 * @param {} event
            	 * @param {} validator
            	 * @return 
            	 */
            	invalidHandler: function (event, validator) { //display error alert on form submit   

	            },

	            /**
            	 * Description
            	 * @method highlight
            	 * @param {} element
            	 * @return 
            	 */
            	highlight: function (element) { // hightlight error inputs
	                $(element)
	                    .closest('.form-group').addClass('has-error'); // set error class to the control group
	            },

	            /**
            	 * Description
            	 * @method success
            	 * @param {} label
            	 * @return 
            	 */
            	success: function (label) {
	                label.closest('.form-group').removeClass('has-error');
	                label.remove();
	            },

	            /**
            	 * Description
            	 * @method errorPlacement
            	 * @param {} error
            	 * @param {} element
            	 * @return 
            	 */
            	errorPlacement: function (error, element) {
	                if (element.attr("name") == "tnc") { // insert checkbox errors after the container                  
	                    error.insertAfter($('#register_tnc_error'));
	                } else if (element.closest('.input-icon').size() === 1) {
	                    error.insertAfter(element.closest('.input-icon'));
	                } else {
	                	error.insertAfter(element);
	                }
	            },

	            /**
            	 * Description
            	 * @method submitHandler
            	 * @param {} form
            	 * @return 
            	 */
            	submitHandler: function (form) {
	                form.submit();
	            }
	        });

			$('.register-form input').keypress(function (e) {
	            if (e.which == 13) {
	                if ($('.register-form').validate().form()) {
	                    $('.register-form').submit();
	                }
	                return false;
	            }
	        });

	        jQuery('#register-btn').click(function () {
	            jQuery('.login-form').hide();
	            jQuery('.register-form').show();
	        });

	        jQuery('#register-back-btn').click(function () {
	            jQuery('.login-form').show();
	            jQuery('.register-form').hide();
	        });
	}
    
    return {
        //main function to initiate the module
        /**
         * Description
         * @method init
         * @return 
         */
        init: function () {
        	
            handleLogin();
            handleForgetPassword();
            handleRegister();        
	       
        }

    };

}();