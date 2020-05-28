import json

file = 'doctors_drugs_reviews.json'  # input('path to file: ') or

taggers = ['polyana', 'egor', 'kuzya', 'andrey']
name = None
while not name:
    name = input('you name: ')
    if name not in taggers:
        print(f'only {taggers} allowed')
        name = None

with open(file, 'r', encoding='utf-8') as f:
    corpora = json.load(f)

if name == 'polyana':
    corpora = corpora[:int(len(corpora)/4)]
elif name == 'egor':
    corpora = corpora[int(len(corpora)/4): int(len(corpora) / 2)]
elif name == 'kuzya':
    corpora = corpora[int(len(corpora)/2):int(len(corpora)*3/4)]
elif name == 'andrey':
    corpora = corpora[int(len(corpora)*3/4):]

print(f'доступно {len(corpora)} вхождений')

try:
    _ = open(f'{name}_log.txt')
except FileNotFoundError:
    with open(f'{name}_log.txt', 'w', encoding='utf-8') as f:
        f.write('0')

with open(f'{name}_log.txt', 'r', encoding='utf-8') as f:
    count = int(f.readlines()[-1])
print(f'из них вы разметили уже {count}')
print('чтобы выйти из разметки и сохранить результат введите out')

with open(f'{name}_output.tsv', 'a', encoding='utf-8') as out:
    go = True
    while go:
        entry = corpora[count]
        minus = entry['comment_minus']
        if minus is None:
            count += 1
            print('skipped, ', count)
            continue

        print('--->', minus)
        tag = input('1 = нет побочки, 2 = побочка, 3 =  не знаю\ntag: ')

        if tag == 'out':
            with open(f'{name}_log.txt', 'a', encoding='utf-8') as f:
                f.write('\n' + str(count))
            print(f'results saved. current count is {count}')
            go = False
        elif tag == '3':
            count += 1
            print('missed, ', count)
            continue
        elif tag == '1' or tag == '2':
            count += 1
            output = []
            for field in ['comment', 'comment_plus', 'comment_minus']:
                text = entry[field]
                if text is None:
                    continue
                output.append(text)

            url = entry['url'].split('/')
            entry_id = url[-3] + "_" + url[-1]
            out.write(f'\n{entry_id}\t{" ".join(output)}\t{int(tag)-1}')

            print('tagged, ', count)

        else:
            print("0 or 1, or 'out' to quit ")
