import { useNavigate } from 'react-router';
import ServiceApi from '../../api/serviceAPI';
import { Breed, PetType, PostPetReport } from '../../api/types';
import styles from './PostReport.module.css'
import { useEffect, useState, useRef } from 'react';
import { authStore } from '../../stores/AuthStore';

const PostReport = () => {
    const navigate = useNavigate();
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);

    const [formData, setFormData] = useState<PostPetReport>({
        user_id: authStore.user!.id,
        breed_id: 0,
        title: '', 
        resolved: false,
        special_marks: '',
        report_type: '',
        location: '',
        description: '',
        picture: null
    });

    const [breeds, setBreeds] = useState<Breed[]>([]);
    const [pets, setPets] = useState<PetType[]>([]);
    const [selectedPet, setSelectedPet] = useState<string>('');
    const [selectedBreed, setSelectedBreed] = useState<number>(-1);
    const [validateErrors, setValidateErrors] = useState<string[]>([]);

    const filteredBreeds = breeds.filter(breed => 
        breed.pet_type_id.type_name === selectedPet
    );

    const fetching = async () => {
        const breedData = await ServiceApi.getBreeds();
        if(breedData.status === 200){
            setBreeds(breedData.data);
            const petElements: PetType[] = [];
            for (const elem of breedData.data) {
                if(petElements.length === 0 || 
                   petElements[petElements.length-1].type_name !== elem.pet_type_id.type_name) {
                    petElements.push(elem.pet_type_id);
                }
            }
            setPets(petElements);
        }
    }

    const handleSubmitClick = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Валидация
        const errors = [];
        if (formData.title.length < 5) errors.push('Заголовок должен состоять из минимум пяти символов');
        if (formData.breed_id <= 0) errors.push('Выбор животного и породы обязателен');
        if (!formData.report_type) errors.push('Нужно выбрать, потеряно или найдено животное');
        if (!formData.description) errors.push('Поле описания обязательно');
        if (!formData.location) errors.push('Укажите локацию');
        if (!formData.special_marks) errors.push('Укажите отличительные знаки');

        if (errors.length > 0) {
            setValidateErrors(errors);
            return;
        }

        try {
            const formDataToSend = new FormData();
            
            // Добавляем все поля в FormData
            Object.entries(formData).forEach(([key, value]) => {
                if (key === 'picture' && value instanceof File) {
                    formDataToSend.append(key, value);
                } else if (key !== 'picture') {
                    formDataToSend.append(key, String(value));
                }
            });

            const response = await ServiceApi.postReport(formDataToSend);
            
            if (response.status === 201) {
                navigate('/reports');
            }
        } catch (error) {
            console.error("Ошибка:", error);
            setValidateErrors(['Ошибка при создании объявления']);
        }
    };

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setFormData({...formData, picture: file});
            
            const reader = new FileReader();
            reader.onload = () => {
                setImagePreview(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    useEffect(() => {
        fetching();
    }, []);

    return (
        <form className={styles.wrapper} onSubmit={handleSubmitClick}>
            {/* Превью изображения */}
            {imagePreview && (
                <div className={styles.imagePreview}>
                    <img src={imagePreview} alt="Предпросмотр" />
                </div>
            )}
            
            {/* Поле для загрузки изображения */}
            <label className={styles.fileInputLabel}>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleImageChange}
                    accept="image/*"
                    className={styles.fileInput}
                />
                {imagePreview ? 'Изменить фото' : 'Добавить фото'}
            </label>

            <label htmlFor="title">Введите заголовок вашего объявления</label>
            <input 
                type="text" 
                name='title' 
                value={formData.title} 
                onChange={(e) => setFormData({...formData, title: e.target.value})}
            />
            
            <div className={styles.options}>
                <select 
                    className={styles.select}
                    value={selectedPet} 
                    onChange={(e) => {
                        setSelectedPet(e.target.value);
                        setSelectedBreed(-1);
                        setFormData({...formData, breed_id: -1});
                    }}
                    required
                >
                    <option value="">-- Выберите животное --</option>
                    {pets.map((item, index) => 
                        <option key={index} value={item.type_name}>
                            {item.type_name}
                        </option>
                    )}
                </select>
                
                {selectedPet && (
                    <select
                        className={styles.select}
                        value={selectedBreed}
                        onChange={(e) => {
                            const breedId = Number(e.target.value);
                            setSelectedBreed(breedId);
                            setFormData({...formData, breed_id: breedId});
                        }}
                        required
                    >
                        <option value="">-- Выберите породу --</option>
                        {filteredBreeds.map((breed) => (
                            <option key={breed.id} value={breed.id}>
                                {breed.breed}
                            </option>
                        ))}
                    </select>
                )}
            </div>

            <label htmlFor="special_marks">Отличительные знаки</label>
            <input
                className={styles.marks__input} 
                type="text" 
                name='special_marks'
                value={formData.special_marks}
                onChange={(e) => setFormData({...formData, special_marks: e.target.value})}
            />
            
            <div className={styles.reportType__wrapper}>
                <button 
                    type='button'
                    className={styles.lost}
                    onClick={() => setFormData({...formData, report_type: 'lost'})}
                    style={{
                        border: `2px solid ${formData.report_type === 'lost' ? '#4CAF50' : '#ccc'}`,
                        backgroundColor: formData.report_type === 'lost' ? '#e8f5e9' : 'white',
                    }}
                >
                    Потеряно
                </button>
                <button 
                    type='button'
                    className={styles.found}
                    onClick={() => setFormData({...formData, report_type: 'found'})}
                    style={{
                        border: `2px solid ${formData.report_type === 'found' ? '#4CAF50' : '#ccc'}`,
                        backgroundColor: formData.report_type === 'found' ? '#e8f5e9' : 'white',
                    }}
                >
                    Найдено
                </button>
            </div>

            <label htmlFor="location">
                Место {formData.report_type === 'found' ? 'нахождения' : 'пропажи'}
            </label>
            <input
                className={styles.location__input} 
                type="text" 
                value={formData.location}
                onChange={(e) => setFormData({...formData, location: e.target.value})}
            />
            
            <label htmlFor="description">Опишите животное</label>
            <textarea
                className={styles.description}
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
            
            {/* Вывод ошибок валидации */}
            {validateErrors.length > 0 && (
                <div className={styles.errorContainer}>
                    {validateErrors.map((error, index) => (
                        <p key={index} className={styles.errorText}>{error}</p>
                    ))}
                </div>
            )}
            
            <button type="submit" className={styles.btn_submit}>
                Создать объявление
            </button>
        </form>
    );
}

export default PostReport;