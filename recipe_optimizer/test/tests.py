import pytest
import json

def calculate_time(steps):
    results = []
    step_times = {}
    chef_busy_until = 0

    while steps:
        current_batch = []  # İşlenecek adımlar

        for step in steps:
            # Ön koşulları kontrol et (listeyi kontrol et)
            if step.prerequisites:
                if not all(prerequisite in step_times for prerequisite in step.prerequisites):
                    continue  # Ön koşullar tamamlanmadı

            # Adımın başlangıç zamanını hesapla
            if step.occupies_chef:
                start_time = chef_busy_until
            else:
                start_time = 0

            # Ön koşul bitiş zamanlarını kontrol et
            if step.prerequisites:
                prerequisite_end_times = [
                    step_times[prerequisite]['end_time']
                    for prerequisite in step.prerequisites
                    if prerequisite in step_times
                ]
                if prerequisite_end_times:
                    start_time = max(start_time, max(prerequisite_end_times))

            # Adımın bitiş zamanını hesapla
            end_time = start_time + step.duration

            # Mevcut adımı ekle
            current_batch.append((step, start_time, end_time))

            # Şef meşgulse, zamanı güncelle
            if step.occupies_chef:
                chef_busy_until = end_time

        # Mevcut adımları işle
        for step, start, end in current_batch:
            step_times[step] = {'start_time': start, 'end_time': end}
            results.append(f"'{step.name}' starts at minute {start} and ends at minute {end}.")

        # İşlenen adımları listeden çıkar
        steps = [step for step in steps if step not in [s for s, _, _ in current_batch]]

    return results
class Step:
    def __init__(self, name, duration, occupies_chef=True, prerequisites=None):
        self.name = name
        self.duration = duration
        self.occupies_chef = occupies_chef
        self.prerequisites = prerequisites if prerequisites else []


# Test verilerini JSON dosyasından yükleme
def load_test_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Test verilerini kullanarak Step nesneleri oluşturma
def steps_from_json(step_data):
    step_dict = {}
    for step_info in step_data:
        step = Step(
            name=step_info["name"],
            duration=step_info["duration"],
            occupies_chef=step_info["occupies_chef"],
            prerequisites=[step_dict[prereq] for prereq in step_info["prerequisites"]]
        )
        step_dict[step.name] = step
    return list(step_dict.values())


# Test verilerini çekip test işlemini yapma
@pytest.mark.parametrize("test_case", load_test_data("test_data.json").items())
def test_calculate_time(test_case):
    test_name, test_data = test_case
    steps = steps_from_json(test_data["steps"])

    # calculate_time fonksiyonunu çalıştır
    results = calculate_time(steps)  # Artık calculate_time'ı tekrar yazmak yerine direkt import ettik

    # Beklenen sonuçları karşılaştır
    expected = test_data["expected"]
    assert results == expected
