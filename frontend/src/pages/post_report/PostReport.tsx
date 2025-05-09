import { useNavigate } from 'react-router';
import ServiceApi from '../../api/serviceAPI';
import { Breed, PetType, PostPetReport } from '../../api/types';
import styles from './PostReport.module.css'
import { useEffect, useState } from 'react';

const PostReport = () => {
    const [formData, setFormData] = useState<PostPetReport>({
        user_id: 1,
        breed_id: 0,
        title: '', 
        resolved: false,
        special_marks: '',
        picture: null,
        report_type: '',
        location: '',
        description: ''
    });

    const [breeds, setBreeds] = useState<Breed[]>([]);
    const [pets, setPets] = useState<PetType[]>([]);
    const [selectedPet, setSelectedPet] = useState<string>('');
    const [selectedBreed, setSelectedBreed] = useState<number>(-1);
    const [validateErrors, setValidateErrors] = useState<string[]>([])
    const navigate = useNavigate();

    // Фильтруем породы по выбранному животному
    const filteredBreeds = breeds.filter(breed => 
        breed.pet_type_id.type_name === selectedPet
    );

    const fetching = async () => {
        const breedData = await ServiceApi.getBreeds();
        if(breedData.status === 200){
            setBreeds(breedData.data);
            const petElements: PetType[] = []
            for (const elem of breedData.data) {
                if(petElements.length === 0){
                    petElements.push(elem.pet_type_id)
                } else if (petElements[petElements.length-1].type_name !== elem.pet_type_id.type_name) {
                    petElements.push(elem.pet_type_id)
                } else {
                    continue
                }
            }
            setPets(petElements)
        } else {
            console.log('ERROR');
        }
    }

    function handleSelectPetChange(petName: string) {
        setSelectedPet(petName);
        setSelectedBreed(-1); // Сбрасываем выбор породы при смене животного
        setFormData({...formData, breed_id: -1});
    }

    function handleSelectBreedChange(breedId: number) {
        setSelectedBreed(breedId);
        setFormData({...formData, breed_id: Number(breedId)});
    }

    const reportTypeActive = (value: string) => ({
        border: `2px solid ${formData.report_type === value ? '#4CAF50' : '#ccc'}`,
        backgroundColor: formData.report_type === value ? '#e8f5e9' : 'white',
    })

    function handleSubmitClick() {

        const errors = []

        if (formData.title.length < 5) {
            errors.push('Заголовок должен состоять из минимум пяти символов');
        } else if (formData.breed_id <= 0) {
            errors.push('Выбор животного и породы обязателен');
        } else if (!formData.report_type) {
            errors.push('Нужно выбрать, потеряно или найдено животное');
        } else if (!formData.description) {
            errors.push('Поле описания животного обязательно к заполнению');
        } else if (!formData.location) {
            errors.push('Укажите локацию');
        } else if(!formData.special_marks) {
            errors.push('Укажите отличительные знаки животного(ошейник, цвет шерсти и т.д.');
        }

        if(errors.length > 0) {
            setValidateErrors(errors)
            return;
        }

        async function postReport() {
            try {
                const response = await ServiceApi.postReport(formData);
                console.log("Успех:", response.data);
            } catch (error) {
                console.error("Ошибка:", error); 
            }
        }
        postReport();
        navigate('/reports')

    }

    useEffect(() => {
        fetching();
    }, []);

    return (
        <>
            <form className={styles.wrapper}>
                <label htmlFor="title">Введите заголовок вашего объявления</label>
                <input type="text" name='title' value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})}/>
                
                <div className={styles.options}>
                    <select 
                        className={styles.select}
                        value={selectedPet} 
                        onChange={(e) => handleSelectPetChange(e.target.value)}
                    >
                        <option value="">-- Выберите животное --</option>
                        {pets.map((item, index) => 
                            <option key={index} value={item.type_name}>
                                {item.type_name}
                            </option>
                        )}
                    </select>
                    
                    {/* Второй select появляется только когда выбрано животное */}
                    {selectedPet && (
                        <>
                            <select
                                className={styles.select}
                                value={selectedBreed}
                                onChange={(e) => handleSelectBreedChange(Number(e.target.value))}
                            >
                                <option value="">-- Выберите породу --</option>
                                {filteredBreeds.map((breed, index) => (
                                    <option key={index} value={breed.id}> {/* Предполагаю, что у Breed есть поле id */}
                                        {breed.breed}
                                    </option>
                                ))}
                            </select>
                        </>
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
                    style={reportTypeActive('lost')}
                    >Потеряно</button>
                    <button 
                    type='button'
                    className={styles.found}
                    onClick={() => setFormData({...formData, report_type: 'found'})}
                    style={reportTypeActive('found')}
                    >Найдено</button>
                </div>
                <label htmlFor="location">Место {formData.report_type=='found' ? 'нахождения' : 'пропажи'}</label>
                    <input
                    className={styles.location__input} 
                    type="text" 
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    />
                <label htmlFor="description">Опишите животное</label>
                    <input 
                    className={styles.description}
                    type="text" 
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    />
                
                <button
                className={styles.btn_submit}
                onClick={(e) => {
                    e.preventDefault();
                    handleSubmitClick();
                }}
                >Создать объявление</button>
            </form>
        </>
    );
}

export default PostReport;

//Чтобы все норм отправлялось, сделай айдишники Number;