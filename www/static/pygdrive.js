var PyGDrive = (function($, undefined){
	var _msg_body = null;
	var _msg_div = null;
	var _locked = 0;

	var self = {
	    comm: function(url, type, data, success, error) {
	    	self.lock_activity();
	    	$.ajax({
	    		url: url,
	    		type: type,
	    		data: data,
	    		success: function(res) {
	    			self.unlock_activity();
	    			success(res);
	    		},
	    		error: function(res) {
	    			self.unlock_activity();
	    			error(res);
	    		}
	    	});
	    },

		register_jquery_folder_field: function (fld, trig, loc) {
			jqtrig = $(trig);
            jqfld = $(fld);
            jqloc = $(loc);
            jqfld.change(function() {
                parts = jqfld.val().split('/');
                if(parts.length > 3) {
                    jqloc.val(parts[2]);
                }
                else {
                    jqloc.val('');
                }
            });
            jqfld.prop('readonly', true);
            jqfld.gdrive('set', {
                'trigger': jqtrig,
                'header': 'Select a folder to synchronize',
                'filter': 'application/vnd.google-apps.folder'
            });
		},

		sync_addgdrive: function(repo, loc) {
			repo = repo.trim();
			loc = loc.trim();
			data = {'action': 'addgdrive', 'repo': repo, 'loc': loc};
			if(repo.length == 0) {
				return;
			}
			s = function(res) {
				msg = (res.code == 0) ? 'Repository added successfully' : 'Error adding repository';
                self.popup_alert(msg, function(){location.reload();})
			};
			f = function() { self.popup_alert('Error adding repository.'); };
            self.comm('/', 'POST', data, s, f);
		},

		sync_syncgdrive: function(repo) {
			data = {'action': 'syncgdrive', 'repo': repo};
			s = function(res) {
                msg = (res.code == 0) ? 'Repository synchronized successfully' : 'Error synchronizing repository';
                self.popup_alert(msg, function(){location.reload();})
			};
			f = function() { self.popup_alert('danger', 'Error synchronizing repository.'); };
            self.comm('/', 'POST', data, s, f);
		},

		sync_delgdrive: function(repo) {
			data = {'action': 'delgdrive', 'repo': repo};
			s = function(res) {
				msg = (res.code == 0) ? 'Repository deleted successfully' : 'Error deleting repository';
				self.popup_alert(msg, function(){location.reload();})
			};
			f = function() { self.popup_alert('Error deleting repository.'); };
            self.comm('/', 'POST', data, s, f);
		},

		sync_delgdrive_confirm: function(repo) {
			self.popup_confirm('Are you sure you want to delete this repository?', function(res) {
				if(res) {
					self.sync_delgdrive(repo);
				}
			});
	    },

		popup_alert: function(msg, fn) {
			bootbox.alert(msg, fn);
		},
		
		popup_confirm: function(msg, fn) {
			bootbox.confirm(msg, fn);
		},
		
		lock_activity: function() {
			_locked += 1;
			if(_locked == 1) {
				$("#modal-overlay").fadeIn();
			}
		},
		
		unlock_activity: function() {
			_locked -= 1;
			if(_locked == 0) {
				$("#modal-overlay").hide();				
			}
		},
	};
	
	return self;
})(jQuery);

