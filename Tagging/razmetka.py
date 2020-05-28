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

try:
    _ = open(f'{name}_output.tsv')
except FileNotFoundError:
    with open(f'{name}_output.tsv', 'w', encoding='utf-8') as f:
        f.write('id\tclass\tplus\tminus\tall\n')

with open(f'{name}_log.txt', 'r', encoding='utf-8') as f:
    count = int(f.readlines()[-1])
print(f'из них вы разметили уже {count}')

print_option = None
while print_option is None:
    print_option = input('print <all> or just <minus>? ')
    if print_option not in ['all', 'minus']:
        print_option = None

print('чтобы выйти из разметки и сохранить результат введите out')

with open(f'{name}_output.tsv', 'a', encoding='utf-8') as out:
    go = True
    while go:
        entry = corpora[count]
        comment = entry['comment']
        plus =  entry['comment_plus']
        all = []
        for field in ['comment', 'comment_plus']:
            text = entry[field]
            if text is None:
                continue
            all.append(text)
        com_plus = ' '.join(all)
        minus = entry['comment_minus']
        if minus is None:
            count += 1
            print('skipped, ', count)
            continue

        if print_option == 'all':
            print('->', com_plus)

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

            com_plus = com_plus.replace('\n', ' ')
            minus = minus.replace('\n', '')

            url = entry['url'].split('/')
            entry_id = url[-3] + "_" + url[-1]
            out.write(f'{entry_id}\t{int(tag)-1}\t{com_plus}\t{minus}\t{" ".join([com_plus, minus])}\n')

            print('tagged, ', count)

        else:
            print("0 or 1, or 'out' to quit ")
