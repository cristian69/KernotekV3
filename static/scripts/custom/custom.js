/**
Custom module for you to write your own javascript functions
**/
var Custom = function () {

    // private functions & variables

    /**
     * Description
     * @method myFunc
     * @param {} text
     * @return 
     */
    var myFunc = function(text) {
        alert(text);
    }

    // public functions
    return {

        //main function
        /**
         * Description
         * @method init
         * @return 
         */
        init: function () {
            //initialize here something.            
        },

        //some helper function
        /**
         * Description
         * @method doSomeStuff
         * @return 
         */
        doSomeStuff: function () {
            myFunc();
        }

    };

}();

/***
Usage
***/
//Custom.init();
//Custom.doSomeStuff();