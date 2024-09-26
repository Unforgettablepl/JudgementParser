from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import re
import requests
import os
import winsound

options = ChromeOptions()
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=options)
driver.get('https://judgments.ecourts.gov.in/pdfsearch/index.php')

input("Press Enter once you have opened the page to be scraped")

print("Fetching the links to be downloaded")
page_html = driver.page_source
to_be_fetched = re.findall(r'open_pdf.*?\.pdf', page_html)
for i in range(len(to_be_fetched)):
    to_be_fetched[i]+=r"');"
    print(to_be_fetched[i])

input("Does that look good? Press Enter to continue")
print("Injecting custom js")

driver.execute_script(
    '''
    open_pdf = function(val, citation_year, path, nc_display) {//alert(1111);
        var file_type = $("#sel_file_type" + val).val();//alert(file_type);
        $('#viewFiles-body').html('');
        var lang_flg = $("#language" + val).val();//alert(path);
        /*if(lang_flg!='' && citation_year=='')
        {
             path=$.session.get(val+"_path");
             citation_year=$.session.get("citation_year");

        }*/
        var fcourt_type = $('#fcourt_type').val();

        var url = "pdf_search/openpdfcaptcha";
        var post_data = 'val=' + val + '&lang_flg=' + lang_flg + '&path=' + path + '&citation_year=' + citation_year + '&fcourt_type=' + fcourt_type + '&file_type=' + file_type + '&nc_display=' + nc_display;
        //ajaxCall(url,post_data,callbk);
        ajaxCall({url: url, postdata: post_data, callback: callbk});

        function callbk(result) {


            if (result.filename != '' && result.filename != undefined) {
                $('#viewFiles').modal('show');
                $('#viewFiles-body').html(result.filename);

                var param = val + ',"' + lang_flg + '","' + path + '",' + citation_year;

                $('#viewFiles-body').append("<input type='button' href='' class='btn btn-success btn-sm col-auto' value='submit'  onclick='get_pdf_dtls(" + param + ");'>")

                $("#modal_close").click(function () {
                    $("#link_" + val).focus();
                });
            } else if (result.outputfile != '' && result.outputfile != undefined) {
                console.log(result.outputfile);
            }
        }
    }
    '''
)

directory = input("Where should the files be downloaded?")
os.makedirs(directory, exist_ok=True)

for i in to_be_fetched:
    success = False
    retrys = 0
    while not success:
        if retrys==10:
            print('\a')
            winsound.Beep(1000, 1000)
            print("Please Fix Error, retried too many times.")
            input("Press Enter to continue retrying")
            retrys = 0
        print("Downloading", i)
        driver.get_log('browser')
        driver.execute_script(i)
        waited = 0
        while True:
            curr = driver.get_log('browser')
            if not curr:
                waited+=1
                time.sleep(1)
                if waited==10:
                    print('\a')
                    winsound.Beep(1000, 1000)
                    print("Timed out creating the pdf link. There may be a captcha")
                    input("Press Enter to continue retrying")
                    waited = 0
                continue
            if curr['level']!='INFO':
                print('\a')
                winsound.Beep(1000,1000)
                input("A severe error occured. Please fix the error and press Enter to continue retrying")
                break
            link = curr[-1]['message']
            link = link.partition('"')[2]
            link = link.partition('"')[0]
            link = "https://judgments.ecourts.gov.in" + link
            file_name = link.split('/')[-1]
            file_path = os.path.join(directory, file_name)
            time.sleep(2)
            response = requests.get(link)
            if response.status_code == 200 and len(response.content)>2000:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print("Downloaded", file_name)
                success = True
                break
            else:
                if response.status_code == 200:
                    print("Failed to download. Error page returned.")
                else:
                    print("Failed to download. Status code:", response.status_code)
                print("Retrying")
                break
        retrys+=1

print("Completed Downloads. Quiting")
driver.quit()
