var Api = "http://127.0.0.1:8026/";


function method_call_post(end_point,data){
    var xhr = new XMLHttpRequest();
    var url = Api + end_point;
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(data);
    if (xhr.status == 201){
        window.alert("Successfully Added")}
    else{
        window.alert(xhr.response)}
};

function method_call_get(end_point) {
    var xhr = new XMLHttpRequest();
    var url = Api + end_point;
    xhr.open( "GET", url, false );
    xhr.send( null );
    return xhr.responseText;
};

function player_register() {
    var endpoint_name = 'player_info';
    var player_name = document.getElementById('first_name').value;
    var email_address = document.getElementById('InputEmail').value;
    var age = document.getElementById('age').value;
    var alias = document.getElementById('alias').value;
    var api_data = JSON.stringify({"player_name":player_name,"email_id":email_address,"age":age,"alias":alias});
    method_call_post(endpoint_name,api_data);
    };

function create_game() {
    var endpoint_name = 'game_info';
    var game_name = document.getElementById('game_name').value;
    var max_teams = document.getElementById('max_teams').value;
    var win_points = document.getElementById('win_points').value;
    var game_desc = document.getElementById('game_desc').value;
    var api_data = JSON.stringify({"game_name":game_name,"max_teams":max_teams,"winning_points":win_points,"game_description":game_desc});
    method_call_post(endpoint_name,api_data);

};

function get_game_list() {
    var endpoint_name = 'game_info';
    return method_call_get(endpoint_name)
};

function set_game_option() {
      var options = JSON.parse(get_game_list());
      var selectBox = document.getElementById('select_game');
      for(var i = 0, l = options.length; i < l; i++){
      var option = options[i];
      selectBox.options.add( new Option(option.game_name));
    };
};

function removeoptions(selectbox) {
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--){
        selectbox.remove(i);
    }
};



function set_player_option() {
    player_data_json = get_player_list();
    player_data = player_data_json.player_data;
    selected_game = document.getElementById('select_game').value;
    valid_players = [];
    player_game_data = player_data_json.game_player_info[selected_game];
    for (index = 0; index < player_game_data.length;++index){
        player_data.splice(player_data.indexOf(player_game_data[index]),1)
    };

    var selectBox = document.getElementById('select_player_1');
    removeoptions(selectBox);
    for(var i = 0, l = player_data.length; i < l; i++){
        var player_key = player_data[i];
        selectBox.options.add( new Option(player_key));
    };

    var selectBox = document.getElementById('select_player_2');
    removeoptions(selectBox);
    for(var i = 0, l = player_data.length; i < l; i++){
        var player_key = player_data[i];
        selectBox.options.add( new Option(player_key));
    };
};

function get_player_list() {
    var endpoint_name = 'player_info';
    var player_list = JSON.parse(method_call_get(endpoint_name));
    player_array = [];
    for (index = 0; index < player_list.length; ++index){
        player_array.push(player_list[index].alias)
    }

    var player_game_info_end_point = 'player_game_info';
    var game_player_data = JSON.parse(method_call_get(player_game_info_end_point));
    response_dict = {};
    response_dict['player_data'] = player_array;
    response_dict['game_player_info'] = game_player_data;
    return response_dict;
};

function team_submit() {
    var endpoint_name = 'team_info';
    var team_name =document.getElementById('team_name').value;
    var game_name =document.getElementById('select_game').value;
    var player_1 =document.getElementById('select_player_1').value;
    var player_2 =document.getElementById('select_player_2').value;
    var api_data = JSON.stringify({"team_name":team_name,"player_1":player_1,"player_2":player_2,"game_name":game_name});
    method_call_post(endpoint_name,api_data);
};

function select_team_option() {
    var endpoint_name = 'team_game_info';
    var team_list_data = JSON.parse(method_call_get(endpoint_name));
    selected_game = document.getElementById('select_game').value;
    var team_list =  team_list_data[selected_game];

    var selectBox = document.getElementById('team_1');
    removeoptions(selectBox);
    for(var i = 0, l = team_list.length; i < l; i++){
        var player_key = team_list[i];
        selectBox.options.add( new Option(player_key));
    };

    var selectBox = document.getElementById('team_2');
    removeoptions(selectBox);
    for(var i = 0, l = team_list.length; i < l; i++){
        var player_key = team_list[i];
        selectBox.options.add( new Option(player_key));
    };
};

function select_winning_teams(){
    var selectBox = document.getElementById('winning_team');
    removeoptions(selectBox);
    team_list = []
    var team_1 = document.getElementById('team_1').value;
    var team_2 = document.getElementById('team_2').value;
    team_list.push(team_1);
    team_list.push(team_2);
    for(var i = 0, l = team_list.length; i < l; i++){
        var player_key = team_list[i];
        selectBox.options.add( new Option(player_key));
    };

};

function winning_submit() {
    var endpoint_name = 'point_decider';
    var team_1 = document.getElementById('team_1').value;
    var team_2 = document.getElementById('team_2').value;
    var winning_team = document.getElementById('winning_team').value;
    var game_name = document.getElementById('select_game').value;
    var api_data = JSON.stringify({"team1":team_1,"team2":team_2,"winning_team":winning_team,"game_name":game_name});
    method_call_post(endpoint_name,api_data);
    };

function get_leaderboard(){
    var endpoint_name = 'leaderboard';
    var game_name = document.getElementById('select_game').value;
    var game_data = JSON.parse(method_call_get(endpoint_name));
    var table = document.getElementById("table_data");
    table.innerHTML = "";
    populateOverallOverview(game_data[game_name])
}



function populateOverallOverview(result) {
    var table = document.getElementById("table_data");

    function addCell(tr, text) {
        var td = tr.insertCell();
        td.textContent = text;
        return td;
    };
    var thead = table.createTHead();
    var headerRow = thead.insertRow();
    addCell(headerRow, '#');
    addCell(headerRow, 'Team Name');
    addCell(headerRow, 'Points');

    var count = 1
    for (var key in result) {
    if (result.hasOwnProperty(key)) {
        var row = table.insertRow();
        addCell(row, count);
        addCell(row, key);
        addCell(row, result[key]);
        count++
        }
    }
};

var nav = '<nav class="navbar navbar-default">\n' +
    '  <div class="container-fluid">\n' +
    '    <!-- Brand and toggle get grouped for better mobile display -->\n' +
    '    <div class="navbar-header">\n' +
    '      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">\n' +
    '        <span class="sr-only">Toggle navigation</span>\n' +
    '        <span class="icon-bar"></span>\n' +
    '        <span class="icon-bar"></span>\n' +
    '        <span class="icon-bar"></span>\n' +
    '      </button>\n' +
    '\n' +
    '    </div>\n' +
    '\n' +
    '    <!-- Collect the nav links, forms, and other content for toggling -->\n' +
    '    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">\n' +
    '      <ul class="nav navbar-nav">\n' +
    '        <li><a href="/">Home</a></li>\n' +
    '        <li><a href="/player_registration">Player Registration</a></li>\n' +
    '        <li><a href="/create_game">Create Game</a></li>\n' +
    '        <li><a href="/create_team">Create Team</a></li>\n' +
    '        <li><a href="/team_decider">Team Decider</a></li>\n' +
    '\n' +
    '\n' +
    '          </ul>\n' +
    '        </li>\n' +
    '      </ul>\n' +
    '    </div><!-- /.navbar-collapse -->\n' +
    '  </div><!-- /.container-fluid -->\n' +
    '</nav>'

function nav_include() {
         document.getElementById("nav-placeholder").innerHTML= nav;

};


