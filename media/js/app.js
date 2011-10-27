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
        checkbox.onClick(function(){
            var inputs = $$("input[type='checkbox']");
            var checked = this._.checked;
            inputs.each(function(item){
                if(item.get('id') != 'select-all')
                    item._.checked = checked;
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
    // form buttons
    if($('delete')) {
        var del = $('delete');
        del.onClick(function(){
            var action = $('action');
            action.set('value', 'delete');
            var form = del.parent('form');
            form.submit();
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
});