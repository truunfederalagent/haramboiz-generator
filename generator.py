from PIL import Image
import os, random, csv, time, json

BACKGROUNDS = '01Backgrounds'
BACK_ACCESSORIES = '02Back Accessories'
FUR = '03Fur'
SKIN = '04Skin'
BODY_OUTLINE = '05BodyOutline'
SHIRTS = '06Shirts'
NECKLACES = '07Necklaces'
JACKETS = '08Jackets'
SHOULDER_ACCESSORIES = '09Shoulder Accessories'
MOUTHS = '10Mouths'
EYES = '11Eyes'
EARRINGS = '14Earrings'
GLASSES = '12Glasses'
HATS = '13Hats'

displays = {
    BACKGROUNDS: 'Background',
    BACK_ACCESSORIES: 'Back Accessory',
    FUR : 'Fur',
    SKIN : 'Skin',
    SHIRTS : 'Shirt',
    NECKLACES : 'Necklace',
    JACKETS : 'Jacket',
    SHOULDER_ACCESSORIES : 'Shoulder',
    MOUTHS : 'Mouth',
    EYES : 'Eyes',
    EARRINGS : 'Earring',
    GLASSES : 'Glasses',
    HATS : 'Hat'
}

time_start = time.time()


all_categories = sorted(os.listdir('assets'), key=lambda p: int(p[:2]))
backgrounds, *categories = all_categories

optional = set([SHIRTS, JACKETS, EARRINGS, GLASSES, HATS])
semi_rare = set([NECKLACES])
rare = set([SHOULDER_ACCESSORIES])
ultra_rare = set([BACK_ACCESSORIES])


start = 1
stop = 2
generate = True


generated = set()
if not os.path.exists('outputs'):
    os.mkdir('outputs')
if not os.path.exists('traits'):
    os.mkdir('traits')


for group in range(start, stop + 1):
    print(group)
    directory = f'outputs/group{group}'
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(f'traits/group_{group}_traits.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=displays.values())
        writer.writeheader()
        for n in range(100):
            selected  = {category:None for category in all_categories}
            bg_dir = f'assets/{backgrounds}'
            bg_asset = f'{bg_dir}/{random.choice(os.listdir(bg_dir))}'
            selected[backgrounds] = bg_asset
            if generate:
                base = Image.open(bg_asset)


            for category in categories:
                cat_dir = f'assets/{category}'

                if category in optional and random.uniform(0, 1) < .4:
                    continue
                
                if category in semi_rare and random.uniform(0, 1) < .7:
                    continue

                if category in rare and random.uniform(0, 1) < .9:
                    continue
                
                if category in ultra_rare and random.uniform(0, 1) < .96:
                    continue

                if selected[JACKETS] and ('Hood' in selected[JACKETS] or 'Onesie' in selected[JACKETS]):
                    if category in [SHOULDER_ACCESSORIES, HATS, EARRINGS, GLASSES]:
                        continue

                assets = os.listdir(cat_dir)
                if category == FUR:
                    tiger = [fur for fur in assets if 'Tiger' in fur]
                    plain = [fur for fur in assets if 'Tiger' not in fur]
                    possible = tiger if random.uniform(0, 1) < .10 else plain
                    asset = random.choice(possible)
                elif category == SKIN:
                    if random.uniform(0, 1) < .2:
                        possible = ['Skin_Marble.png', 'Skin_Acid2.png', 'Skin_Acid2.png', 'Skin_Camo.png', 'Skin_Camo.png', 'Skin_Camo.png', 'Skin_Crocodile.png', 'Skin_Crocodile.png', 'Skin_Crocodile.png']
                    else:
                        possible = ['Skin_Blue.png', 'Skin_Green.png', 'Skin_Normal.png', 'Skin_Red.png', 'Skin_White.png', 'Skin_Yellow.png']          
                    asset = random.choice(possible)
                elif category == NECKLACES:
                    possible = assets
                    if selected[SHIRTS]:
                        shirt = selected[SHIRTS]
                        if 'Tie' in shirt or 'Button' in shirt or 'VNeck' in shirt:
                            continue
                        elif 'Turtle' in shirt:
                            possible = [n for n in possible if 'Thin' not in n]
                    asset = random.choice(possible)
                elif category == JACKETS:
                    if selected[NECKLACES] and 'Glow' in selected[NECKLACES]:
                        continue
                    possible = []
                    for asset in assets:
                        if selected[SHIRTS]:
                            if 'Hood' in asset or 'Onesie' in asset:
                                continue
                            if 'Button' in selected[SHIRTS] and 'Flannel' in asset:
                                continue
                        possible.append(asset)
                    
                    if random.uniform(0, 1) < .8:
                        possible = [a for a in possible if 'Space' not in a and 'Armor' not in a]
                    
                    asset = random.choice(possible)
                elif category == SHOULDER_ACCESSORIES:
                    possible = assets
                    if selected[BACK_ACCESSORIES]:
                        possible = [asset for asset in possible if 'Guitar' not in asset]
                    
                    if selected[JACKETS] and 'Flannel' in selected[JACKETS]:
                        possible = [asset for asset in possible if 'Guitar' not in asset]
                    if selected[NECKLACES] and 'Glow' in selected[NECKLACES]:
                        possible = [asset for asset in possible if 'Headphone' not in asset]

                    if random.uniform(0, 1) < .5:
                        possible = [asset for asset in possible if 'Kitten' not in asset]    
                    asset = random.choice(possible)
                elif category == MOUTHS:
                    pacifiers = [mouth for mouth in assets if 'Pacifier' in mouth]
                    mouths = [mouth for mouth in assets if 'Pacifier' not in mouth]
                    if random.uniform(0, 1) < .07:
                        possible = pacifiers
                    else:
                        fur = selected['03Fur']
                        fur = fur[fur.find('_') + 1:fur.find('.')]
                        skin = selected['04Skin']
                        skin = skin[skin.find('_') + 1:skin.find('.')]
                        possible = []
                        for asset in mouths:
                            if 'Fur' in asset and f'{fur}Fur' not in asset:
                                continue
                            elif 'Skin' in asset and f'{skin}Skin' not in asset:
                                continue
                            if 'Yawn' in asset and random.uniform(0, 1) < .2:
                                continue
                            possible.append(asset)
                    asset = random.choice(possible)
                elif category == EYES:
                    possible = []
                    skin = selected['04Skin']
                    skin = skin[skin.find('_') + 1:skin.find('.')]
                    for asset in assets:
                        if f'{skin}Skin' in asset:
                            if ('Yawn' in selected[MOUTHS] or 'Tongue' in selected[MOUTHS])  and 'Angry' in asset:
                                continue
                            possible.append(asset)
                    if random.uniform(0, 1) < .7:
                        possible = [eye for eye in possible if 'Glow' not in eye]
                    asset = random.choice(possible)
                elif category == GLASSES:
                    if random.uniform(0, 1) < .6:
                        continue
                    if selected[MOUTHS] and 'Yawn' in selected[MOUTHS]:
                        continue
                    if 'Glow' in selected[EYES]:
                        continue
                    if random.uniform(0, 1) < .8:
                        assets = [glass for glass in assets if 'Laser' not in glass]
                    asset = random.choice(assets)
                elif category == HATS:
                    trilby = [hat for hat in assets if 'Trilby' in hat]
                    non_trilby = [hat for hat in assets if 'Trilby' not in hat]
                    non_trilby.remove('Hats_PrisonCap_Striped.png')
                    if selected[SHIRTS] and 'Prison' in selected[SHIRTS]:
                        possible = ['Hats_PrisonCap_Striped.png']
                    elif random.uniform(0, 1) < .15:
                        possible = trilby
                    elif selected[GLASSES]:
                        possible = [hat for hat in non_trilby if not any(el in hat for el in ('Bike', 'Headphone', 'Tricorn'))]
                        if 'Eyepatch' in selected[GLASSES]:
                            possible = [hat for hat in possible if 'Headband' not in hat]
                    elif selected[SHOULDER_ACCESSORIES]:
                        possible = [hat for hat in non_trilby if not any (el in hat for el in ('Army', 'Bike'))]
                        if 'Headphones' in selected[SHOULDER_ACCESSORIES] or 'Parrot' in selected[SHOULDER_ACCESSORIES]:
                            possible = [hat for hat in possible if 'Headphones' not in hat]
                    else:
                        possible = non_trilby
                    asset = random.choice(possible)
                elif category == EARRINGS:
                    if selected[HATS] and ('Headphones' in selected[HATS] or 'Army' in selected[HATS]):
                        continue
                    possible = []
                    skin = selected['04Skin']
                    skin = skin[skin.find('_') + 1:skin.find('.')]
                    for asset in assets:
                        if 'Skin' in asset and f'{skin}Skin' not in asset:
                            continue
                        possible.append(asset)
                    asset = random.choice(possible)
                else:
                    asset = random.choice(assets)
                
                asset_path = f'{cat_dir}/{asset}'
                selected[category] = asset_path       

            layers = list(selected.items())
            if selected[GLASSES] and selected[HATS] and ('Headband' in selected[HATS] or 'Cap' in selected[HATS]):
                layers[11], layers[12] = layers[12], layers[11]

            combo = tuple(layers)
            if combo not in generated:
                generated.add(combo)
                for category, asset in layers:
                    if generate and asset:
                        layer = Image.open(asset)
                        base = Image.alpha_composite(base, layer)
                meta = {displays[key]: value if value else 'None' for key, value in selected.items() if key in displays}
                writer.writerow(meta)
                if generate:
                    base.save(f'{directory}/haramboi{n}.png')
            else:
                print('repeat found', combo)

with open('generated.json', 'w') as f:
    f.write(json.dumps(list(generated), indent=2))
print(time.time() - time_start)