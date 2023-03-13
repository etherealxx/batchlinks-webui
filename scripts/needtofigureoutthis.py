#justcheckcivit
def civitdown2_get_json(url):
  import re
  m = re.search(r'https://civitai.com/models/(\d+)', url)
  model_id = m.group(1)

  api_url = "https://civitai.com/api/v1/models/" + model_id

  import requests
  txt = requests.get(api_url).text

  import json
  try:
    return json.loads(txt)
  except json.decoder.JSONDecodeError:
    return 'error'
  
model = civitdown2_get_json('https://civitai.com/models/4384/dreamshaper') #'https://civitai.com/models/17277/realism-engine' #https://civitai.com/models/5245/kotosmix
print(model)

def civitmodeltypechooser(modeljson, torchortensor, prunedmodel, linkandnames):

  prunedorfull = []
  if prunedmodel == True:
    prunedorfull = ['?type=Pruned%20Model', '?type=Model']
  else:
    prunedorfull = ['?type=Model', '?type=Pruned%20Model']
  print(str(prunedorfull))

  pickleorsafe = ['&format=SafeTensor', '&format=PickleTensor']
  if torchortensor== 'ckpt':
    pickleorsafe.reverse()

  defaultlinkurl = str([link.get('downloadUrl') for link in modeljson['modelVersions'][0]['files'] if not '?type=' in link.get('downloadUrl')][0])

  # activelink = []
  indexnamelink = []
  for pruned_or_full in prunedorfull:
      for pickle_or_safe in pickleorsafe:
          templink = f"{defaultlinkurl}{pruned_or_full}{pickle_or_safe}"
          for index, (name, link) in enumerate(linkandnames.items()):
              print("is " + templink.split("/")[-1] + " equal to" + link.split("/")[-1] + " ? ")
              if templink == link:
                  indexnamelink = [index, name, link]
                  print(str(indexnamelink))
                  # print(index)
                  # print(name)
                  # print(link)
                  break
          else:
              continue
          break
      else:
          continue
      break
  else:
    for pruned_or_full in prunedorfull:
        for pickle_or_safe in pickleorsafe:
            templink = f"{defaultlinkurl}{pruned_or_full}{pickle_or_safe}"
            for index, (name, link) in enumerate(linkandnames.items()):
                if link == defaultlinkurl:
                    indexnamelink = [index, name, link]
                    print(str(indexnamelink))
                    # print(index)
                    # print(name)
                    # print(link)
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        pass
  
  print(str(indexnamelink))
  return indexnamelink
           
        # print(templink)
        # searcher = 'findstr'
        # try:
        #     link_and_code = [line for line in subprocess.getoutput(f"curl -sI {templink} | {searcher} -i content-disposition").splitlines() if line.startswith('location')][0] #subprocess.getoutput(f"curl -sI {templink}") #getrequest(f"{defaultlinkurl}{pruned_or_full}{pickle_or_safe}")
        #     activelink.append(templink)
        #     print(link_and_code)
        # except:
        #    pass
  # print(str(activelink))
  # try:
  #   return activelink[0]
  # except:
  #   return defaultlinkurl


# for link in model['modelVersions'][0]['files'][0]['downloadUrl']:
#   url = link.get('downloadUrl')
#   if url:
#     print(link)
# data_url = model['modelVersions'][0]['files'][1]['downloadUrl']
# data_filename = model['modelVersions'][0]['files'][1]['name']
linkandname = dict() #list of tuples
for i, link in enumerate(model['modelVersions'][0]['files']):
    name = link.get('name')
    url = link.get('downloadUrl')
    if name and url:
        linkandname[name] = url
        # print(name, url)
        # # print(i, url)
        # print(f"model['modelVersions'][0]['files'][{i}]['downloadUrl']")
    else:
        # handle the case where the url is not present
        pass
print(str(linkandname))
print()
data_url = civitmodeltypechooser(model, 'safetensors', False, linkandname) #@note
print("returned value: " + str(data_url))

    # if url2:
    #     print(i, url2)
    #     print(f"model['modelVersions'][0]['files'][{i}]['name']")
    # else:
    #     # handle the case where the url is not present
    #     pass