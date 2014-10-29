<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <style>
        #modal-overlay{
            position:absolute;
            top:0;
            z-index:10;
            background:black;
            display:block;
            opacity:.75;
            filter:alpha(opacity=75);
            width:100%;
            height:100%;
        }
    </style>
    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/bootbox.js/4.2.0/bootbox.min.js"></script>
    <script src="//apis.google.com/js/client.js"></script>
    <script src="/static/jquery-gdrive.js"></script>
    <script src="/static/pygdrive.js"></script>
    <script>
    	$(document).ready(function() {
    		$('.syncgdrive').click(function(event){
    			repo = event.target.id.split('_')[1];
    			PyGDrive.sync_syncgdrive(repo);
    		});
    		
    		$('.delgdrive').click(function(event){
    			repo = event.target.id.split('_')[1];
    			PyGDrive.sync_delgdrive_confirm(repo);
    		});

    		$('#addgdrive').click(function(event){
    			gfolder = $('#gfolder').val();
    			loc = $('#gfolderloc').val();
    			PyGDrive.sync_addgdrive(gfolder, loc);
    		});

            $().gdrive('init', {
                'devkey': '{{browser_api_key}}',
                'appid': '{{appid}}',
                'authtok': '{{authtok}}',
               	'user': '{{user_id}}'
            });

            PyGDrive.register_jquery_folder_field('#gfolder', '#gfolder_selector', '#gfolderloc');
    	});    	
    </script>
</head>

{% import os %}

<body>
    <div class="container">
        <div class="navbar navbar-default" role="navigation">
            <div class="container-fluid">
                    <span class="navbar-brand"><img src="/static/icons/product32.png"> Google Drive&trade; Sync (pygdrive)</span>
                    <span class="navbar-right" style="padding: 15px; color: #666">{{user_id}}</span>
            </div>
        </div>

        <table class="table table-striped">
            <tr><th>Google Drive Folder</th><th>Local Folder</th><th>Action</th></tr>
            {% for repokey,repo in gdrive_repos.iteritems() %}
                {% set reponame = os.path.basename(repo.loc) %}
                {% set loc = repo.loc %}
                <tr>
                    <td><small>{{loc}}</small></td>
                    <td><b>{{reponame}}</b></td>
                    <td>
                        <span class="glyphicon glyphicon-refresh syncgdrive btn" id="syncgdrive_{{repokey}}" title="Synchronize with Google Drive"></span>
                        <span class="glyphicon glyphicon-trash delgdrive btn" id="delgdrive_{{repokey}}" title="Delete from JuliaBox"></span>
                    </td>
                </tr>
            {% end %}
            <tr>
                <td>
                    <table width="100%">
                        <tr>
                            <td><input type="text" id="gfolder" class="form-control"></td>
                            <td><span class="glyphicon glyphicon-folder-open btn" id="gfolder_selector" title="Select Google Drive folder"></span></td>
                        </tr>
                    </table>
                </td>
                <td><input type="text" id="gfolderloc" class="form-control"/></td>
                <td><span class="glyphicon glyphicon-plus btn" id="addgdrive" title="Add for sync"></span></td>
            </tr>
        </table>
    </div>
    <div id="modal-overlay" style="display: none;"></div>
</body>
</html>