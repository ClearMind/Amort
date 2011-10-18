/**
 * Created by PyCharm.
 * User: cm
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
});