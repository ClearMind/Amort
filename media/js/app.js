/**
 * Created by PyCharm.
 * User: Clear_Mind
 * Date: 12.10.11
 * Time: 14:17
 * To change this template use File | Settings | File Templates.
 */

$(document).onReady(function() {
    if($('id_fio')) {
        var completer = new Autocompleter('id_fio', {
            url: '/user/%{search}',
            minLength: 3
        });
        $('id_fio').on({
            blur: function() {
                var name = this.value();
                xhr = new Xhr('/user_info/' + name, {
                    method: "get",
                    onSuccess: function() {
                        var json = this.responseJSON;
                        if(json.tab_number) {
                            $('id_tab_number').setValue(json.tab_number);
                            $('id_post').setValue(json.post);
                            $('id_cabinet').setValue(json.cabinet);
                        }
                    }
                }).send();
            }
        });
    }
    // select/unselect all
    if($('select-all')) {
        var checkbox = $('select-all');
        var inputs = $$('table.data input[type="checkbox"]');
        checkbox.onClick(function(){
            var checked = this.checked();
            inputs.each(function(item){
                if(item.get('id') != 'select-all')
                    item.checked(checked);
                    item.fire("change");
            });
        });
        inputs.each(function(item){
            item.onChange(function(e){
                var tr = e.target.parent('tr');
                if(e.target.checked())
                    tr.setStyle({ background: "#4ADEFF"});
                else
                    tr.setStyle({ background: "white"});
            });
        });
    }
    // gen doc request
    if($$('.doc')) {
        $$('.doc').each(function(item){
            item.onClick(function(){
                var id = this.get('id');
                var xhr = new Xhr("/get_url/request/", {
                    params: {id: id},
                    method: "post",
                    spinner: $('spinner-' + id),
                    onSuccess: function() {
                        $('down').set('src', this.responseText);
                    }
                }).send();
            });
        });
    }

    // gen act doc url
    if($$('.task_doc')) {
        $$('.task_doc').each(function(item){
            item.onClick(function(){
                var id = this.get('id');
                var xhr = new Xhr("/get_url/task/", {
                    params: {id: id},
                    method: "post",
                    spinner: $('spinner-' + id),
                    onSuccess: function() {
                        $('down').set('src', this.responseText);
                    }
                }).send();
            });
        });
    }

    if($$('.del')) {
        $$('.del').each(function(item){
            item.onClick(function(){
                var id = this.get('id');
                id = id.substr(4, id.length);
                var xhr = new Xhr('/delete_request/', {
                    params: {id: id},
                    method: 'post',
                    spinner: $('del-spinner-' + id),
                    onSuccess: function(request) {
                        var resp = request.responseText;
                        console.log(resp);
                        if(resp == 'OK') {
                            $('del-'+id).parent('tr').fade();
                        }
                    }
                }).send();
            });
        });
    }

    // Selected rows count
    $(document).selected_count = function() {
        var inputs = $$('table.data input[type="checkbox"]');
        var count = 0;
        inputs.each(function(item){
            if(item.get('id') != 'select-all')
                if(item.checked()) {
                    count++;
                }
        });
        return count;
    }
    
    // form buttons
    if($('delete')) {
        var del = $('delete');
        del.onClick(function(){
            if($(document).selected_count() > 0) {
                var action = $('action');
                action.set('value', 'delete');
                var form = del.parent('form');
                form.submit();
            } else {
                $$('.button-message')[0].fade("in");
                $$('.button-message')[0].fade("out");
            }
        });
    }
    if($('new_task')) {
        var nt = $('new_task');
        nt.onClick(function(){
            var action = $('action');
            action.set('value', 'new_task');
            var form = nt.parent('form');
            form.submit();
        });
    }
    if($('delete_from_task')) {
        var dft = $('delete_from_task');
        dft.onClick(function(){
            if($(document).selected_count() > 0) {
                var action = $('action');
                action.set('value', 'delete_from_task');
                var form = dft.parent('form');
                form.submit();
            } else {
                $$('.button-message')[0].fade("in");
                $$('.button-message')[0].fade("out");
            }
        });
    }
    if($('undo')) {
        var undo = $('undo');
        undo.onClick(function(){
            if($(document).selected_count() > 0) {
                var action = $('action');
                action.set('value', 'undo');
                var form = undo.parent('form');
                form.submit();
            } else {
                $$('.button-message')[0].fade("in");
                $$('.button-message')[0].fade("out");
            }
        });
    }

    var selects = $$('select.status');
    if(selects) {
        selects.each(function(item){
            item.onChange(function(){
                // get row id (task id)
                var tr = this.parent('tr');
                var id = tr.get('id');
                var value = this.value();
                //xhr again
                var xhr = new Xhr("/task_status/", {
                    params: {id: id, value: value},
                    method: "post",
                    spinner: $('spinner-' + id),
                    onSuccess: function(request) {
                        console.log(request.responseText);
                        if(value == 'ended') {
                            $(id).fade();
                        }
                    }
                }).send();
            });
        });
    }
});