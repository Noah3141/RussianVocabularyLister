# Detection (as in compiler) needs to occur before these entries are changed for appearances

def front_face_trees(tree_dictionary):
    try:tree_dictionary["хвалить"][0] = "-хваливать, -хвалять"
    except: pass
    try:tree_dictionary["класть"][0] = "-кладывать), *ложить (-лагать"
    except: pass
    try:
        tree_dictionary["глотать"][0] = "-глатывать), *глотить (-глощать"
        tree_dictionary["глотать"][1] = tree_dictionary["глотать"][1] + "  по-  пере-  на-"
    except: pass
    try:tree_dictionary["бодрить"][0] = "-бадривать, -бадрять"
    except: pass
    try:tree_dictionary["лететь"][0] = "-летать, -лётывать"
    except: pass
    try:tree_dictionary["бодрить"][0] = "-рождать, -рожать"
    except: pass
    try:tree_dictionary["нести"][0] = "-носить, -нашивать"
    except: pass
    try:tree_dictionary["трогать"][0] = "-трагивать, -трогивать"
    except: pass
    try:tree_dictionary["давить"][0] = "-давлять, -давливать"
    except: pass
    try:tree_dictionary["целить"][0] = "-целять (целый), -целивать (цель)"
    except: pass
    try:tree_dictionary["рядить"][0] = "-ряжать, -ряживать"
    except: pass
    try:tree_dictionary["дарить"][0] = "-даривать, -дарять"
    except: pass
    try:tree_dictionary["нять"][0] = "-нимать), ять (-имать"
    except: pass
    try:tree_dictionary["орать"] = ("-*","")
    except: pass
    try:tree_dictionary["жевать"][0] = "-жёвывать"
    except: pass
    try:tree_dictionary["стегать"][0] = "-стёгивать"
    except: pass
    try:tree_dictionary["вертеть"][0] = "-вёртывать"
    except: pass
    try:tree_dictionary["метать"][0] = "-мётывать"
    except: pass
    try:tree_dictionary["плескать"][0] = "-плёскивать"
    except: pass
    try:tree_dictionary["лежать"][0] = "-лёживать"
    except: pass
    try:tree_dictionary["веять"][0] = "-вевать, -веивать"
    except: pass
    try:tree_dictionary["кушать"][0] = "-кушивать, -кусывать"
    except: pass
    try:tree_dictionary["тесать"][0] = "-тёсывать"
    except: pass
    try:
        tree_dictionary["дёргать"] = tree_dictionary["дергать"]
        del tree_dictionary["дергать"]
        tree_dictionary["дёргать"][0] = "-дёргивать"
    except: pass
    
    try:tree_dictionary["клевать"][0] = "-клёвывать"
    except: pass
    try:tree_dictionary["черкать"][0] = "-чёркивать"
    except: pass
    try:tree_dictionary["хлестать"][0] = "-хлёстывать"
    except: pass
    
    try:
        tree_dictionary["-вратить"] = tree_dictionary["вратить"]
        del tree_dictionary["вратить"]
        tree_dictionary["-вратить"][0] = "-вращать"
    except: pass

    try:
        tree_dictionary["таскать, тащить"] = tree_dictionary["таскать"]
        del tree_dictionary["таскать"]
        tree_dictionary["таскать, тащить"][0] = "-таскивать"
    except: pass

    try:
       tree_dictionary["ходить, идти"] = tree_dictionary["ходить"]
       del tree_dictionary["ходить"]
       tree_dictionary["ходить, идти"][0] = "-ходить, -хаживать"
    except: pass

    try:
        tree_dictionary["ехать"][0] = "*)  ездить (-езжать"
    except: pass

    try:
        tree_dictionary["лезть"][0] = "-лезать) лазить (-лазать"
    except: pass

    try:
        tree_dictionary["-требить"] = tree_dictionary["требить"]
        del tree_dictionary["требить"]
        tree_dictionary["-требить"][0] = "-треблять"
    except: pass


    try:
        tree_dictionary["-становить"] = tree_dictionary["становить"]
        del tree_dictionary["становить"]
        tree_dictionary["-становить"][0] = "-становлять, -станавливать"
    except: pass

    try:
        tree_dictionary["-личить"] = tree_dictionary["личить"]
        del tree_dictionary["личить"]
        tree_dictionary["-личить"][0] = "-личать"
    except: pass

    try:
        tree_dictionary["-прячь"] = tree_dictionary["прячь"]
        del tree_dictionary["прячь"]
        tree_dictionary["-прячь"][0] = "-прягать"
    except: pass


    # Sorting tree dictionary by length of prefix list

    tree_dict_sub = dict()
    prefixes_length = dict()

    for key in tree_dictionary:
        prefixes_length[key] = len(tree_dictionary[key][1].split("- "))
        if tree_dictionary[key][1].split("- ")[0] == "":
            prefixes_length[key] = 0
        
    prefixes_length = sorted(prefixes_length, key = lambda x: prefixes_length[x], reverse=True)

    for key in prefixes_length:
        tree_dict_sub[key] = tree_dictionary[key]

    tree_dict = tree_dict_sub



    tree_dict["*"] = ("Bushes - some prefixed forms exists, but not branch imperfectives","")

    return tree_dict