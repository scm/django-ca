django.jQuery(document).ready(function() {
    var ca_profiles;
    var profile_selector = '.field-profile select'
    var profile_url = django.jQuery('meta[name="get-profiles-url"]').attr('value');

    django.jQuery.get(profile_url).done(function(data) {
        ca_profiles = data;

        // set the "fetched" property, this can be used by selenium tests to wait until this API has returned
        django.jQuery('meta[name="get-profiles-url"]').attr('fetched', "true");
    });


    // This should be set in the form via intial
    //var initial_profile = django.jQuery(profile_selector).val();

    django.jQuery(profile_selector).change(function() {
        if (this.value == '') {
            django.jQuery('.field-profile .profile-desc').hide();
            return;  // do nothing if we don't select a profile
        }

        var profile = ca_profiles[this.value];
        var subject = profile.subject;

        // update subject input field
        django.jQuery.each({
            "C": django.jQuery('.field-subject #country input'),
            "ST": django.jQuery('.field-subject #state input'),
            "L": django.jQuery('.field-subject #location input'),
            "O": django.jQuery('.field-subject #organization input'),
            "OU": django.jQuery('.field-subject #organizational-unit input'),
            "CN": django.jQuery('.field-subject #commonname input'),
            "emailAddress": django.jQuery('.field-subject #e-mail input'),
        }, function(key, input) {
            input.val('' ? typeof subject[key] === 'undefined' : subject[key]);
        });

        // set wether to include the CommonName in the subjectAltName
        cn_in_san = '.field-subject_alternative_name .labeled-checkbox input';
        if (typeof profile.cn_in_san === 'undefined' || profile.cn_in_san) {
            django.jQuery(cn_in_san).prop('checked', true);
        } else {
            django.jQuery(cn_in_san).prop('checked', false);
        }

        if (typeof profile.extensions !== 'undefined') {
            django.jQuery.each(profile.extensions, function(key, ext) {
                var field = django.jQuery('.form-row.field-' + key);
                var critical = ext !== null && ext.critical === true;

                // profile serialization will make sure that any not-null extension will have a critical value
                field.find('.labeled-checkbox.critical input').prop('checked', critical);

                if (key == 'ocsp_no_check') {
                    field.find('.labeled-checkbox.include input').prop('checked', ext !== null);
                    field.find('.labeled-checkbox.include input').change();  // so any existing callbacks are called

                // handle "multiple choice" extensions
                } else if (['extended_key_usage', 'key_usage', 'tls_feature'].includes(key)) {
                    if (ext == null) {
                        field.find('select').val([]);
                    } else {
                        field.find('select').val(ext.value);
                    }
                    field.find('select').change();  // so any existing callbacks are called
                } else if (key === "authority_information_access") {
                    if (ext.value.issuers) {
                        field.find('textarea.ca-issuers').val(ext.value.issuers.join("\n"));
                    }
                    if (ext.value.ocsp) {
                        field.find('textarea.ocsp').val(ext.value.ocsp.join("\n"));
                    }
                } else {
                    console.log("Unhandled extension: " + key);
                }

            });
        }

        // update description
        django.jQuery('.field-profile .profile-desc').show();
        django.jQuery('.field-profile .profile-desc').text(profile.description);
    });
});
