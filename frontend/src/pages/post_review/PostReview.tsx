import { useEffect, useState } from 'react';
import styles from './PostReview.module.css';
import {type PostReview } from '../../api/types';
import { FaStar } from 'react-icons/fa';
import { useNavigate } from 'react-router';
import ServiceApi from '../../api/serviceAPI';

const PostReview = () => {

    const navigate = useNavigate()
    const [validateErrors, setValidateErrors] = useState<string[]>();
    const [formData, setFormData] = useState<PostReview>({
        photo: null,
        text: '',
        rating: 0
    })

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setFormData({...formData, photo: file});
        }
    };

    useEffect(() => {
        window.scroll(0, 0);
    }, [])

    const handleSubmitClick = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Валидация
        const errors = [];
        if (formData.text.length === 0) errors.push('Отзыв должен сожержать символы');
        if (formData.rating === 0) errors.push('Нужно обязательно поставить оценку');

        if (errors.length > 0) {
            setValidateErrors(errors);
            return;
        }

        try {
            const formDataToSend = new FormData();
            
            // Добавляем все поля в FormData
            Object.entries(formData).forEach(([key, value]) => {
                if (key === 'photo' && value instanceof File) {
                    formDataToSend.append(key, value);
                } else if (key !== 'photo') {
                    formDataToSend.append(key, String(value));
                }
            });

            const response = await ServiceApi.postReview(formDataToSend);
            
            if (response.status === 201) {
                navigate('');
            }
        } catch (error) {
            console.error("Ошибка:", error);
            setValidateErrors(['Ошибка при создании объявления']);
        }
    };

    return (
        <form className={styles.form}>
            <label className={styles.fileInputLabel}>
                <input
                    type="file"
                    onChange={handleImageChange}
                    accept="image/*"
                    className={styles.fileInput}
                />
            </label>
            <label htmlFor="rating">Поставьте оценку</label>
                <div className={styles.stars}>
                {[1, 2, 3, 4, 5].map(num => 
                    <FaStar
                        className={styles.star} 
                        key={num}
                        color={num <= formData.rating ? "#008000" : "#D3D3D3"}
                        onClick={() => setFormData({...formData, rating: num})}
                    />
                )}
                </div>
            <label htmlFor="text">Введити текст отзыва:</label>
                <textarea
                className={styles.textArea}
                required
                value={formData.text}
                onChange={e => setFormData({...formData, text: e.target.value})}
                />
            
            <button className={styles.submitBtn} onClick={handleSubmitClick}>
                Оставить отзыв
            </button>
            {validateErrors && validateErrors.map(item =>
                <p>{item}</p>
            )}
        </form>
    );
}
 
export default PostReview;