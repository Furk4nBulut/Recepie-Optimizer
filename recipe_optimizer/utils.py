def calculate_time(steps):
    results = []
    step_times = {}
    chef_busy_until = 0
    last_end_time = 0

    while steps:
        current_batch = []  # İşlenecek adımlar

        for step in steps:
            # Ön koşulları kontrol et
            if step.prerequisites.exists():
                if not all(prerequisite in step_times for prerequisite in step.prerequisites.all()):
                    continue  # Ön koşullar tamamlanmadı

            # Adımın başlangıç zamanını hesapla
            if step.occupies_chef:
                # Eğer adım şef gerektiriyorsa
                start_time = chef_busy_until
            else:
                # Şef gerektirmiyorsa, başlangıç zamanı 0'dan başlar
                start_time = 0

            # Ön koşul bitiş zamanlarını kontrol et
            if step.prerequisites.exists():
                prerequisite_end_times = [
                    step_times[prerequisite]['end_time']
                    for prerequisite in step.prerequisites.all()
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
            last_end_time = max(last_end_time, end)

        # İşlenen adımları listeden çıkar
        steps = [step for step in steps if step not in [s for s, _, _ in current_batch]]

    return results, last_end_time
