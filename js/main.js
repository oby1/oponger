(function(){

    $(function() {

        // Score validation functions
        function is_valid_score(score) {
            return 0 <= score && score < 100;
        }

        function is_int(score) {
            return Number(score) === parseInt(score);
        }

        function is_min_points_to_win(score_1, score_2) {
            return score_1 >= 21 || score_2 >= 21;
        }

        function is_min_spread(score_1, score_2) {
            return Math.abs(score_1 - score_2) >= 2;
        }

        // Attach dialog to complete game link
        $('.complete-game').click(function(){
            $('#complete-game-wrapper').dialog({
                closeText: 'hide',
                draggable: false,
                modal: true,
                resizable: false,
                width: 500
            });
        });

        // Attach form validation to all complete-game forms
        $('#complete-game-form').submit(function() {

            // Get all of the input values
            var $inputs = $(':input', this);
            var values = {};
            $inputs.each(function() {
                values[this.name] = $(this).val();
            });

            // Run some simple sanity checks
            if(!values.player_1_score || !values.player_2_score) {
                $('.error', this).html('Player scores are required.');
                return false;
            }

            if(!is_int(values.player_1_score) || !is_int(values.player_2_score)) {
                $('.error', this).html('Player scores must be valid integers.');
                return false;
            }

            var player_1_score = parseInt(values.player_1_score);
            var player_2_score = parseInt(values.player_2_score);

            if(!is_valid_score(player_1_score) || !is_valid_score(player_2_score)) {
                $('.error', this).html('Player scores must be between 0 and 100.');
                return false;
            }

            if(!is_min_points_to_win(player_1_score, player_2_score)) {
                $('.error', this).html('One of the player scores must be larger than 21.');
                return false;
            }

            if(!is_min_spread(player_1_score, player_2_score)) {
                $('.error', this).html('The point spread must be at least 2.');
                return false;
            }

            return true;
        });

    });

})();
