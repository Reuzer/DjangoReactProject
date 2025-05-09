import { useEffect, useState } from "react";
import { PetReport, PostPetReport } from "../../api/types";
import { useNavigate, useParams } from "react-router-dom";
import ServiceApi from "../../api/serviceAPI";
import styles from './Report.module.css'
import Img from '../../components/Img/Img';
import altPhoto from '../../assets/alter.svg';
import { Modal } from "../../components/modal/Modal";

const Report = () => {

    const navigate = useNavigate();

    const {id} = useParams();
    const [report, setReport] = useState<PetReport>()
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentFormData, setCurrentFormData] = useState<PostPetReport>();
    const [validateErrors, setValidateErrors] = useState<string[]>()
    
    const fetching = async () => {
        const data = await ServiceApi.getReport(Number(id))
        if(data.status === 200) {
            if(!data.data.picture) {
                data.data.picture = 'no picture';
            }
            setReport(data.data);
            setCurrentFormData({
                user_id: data.data.user_id.id,
                breed_id: data.data.breed_id.id,
                title: data.data.title,
                resolved: data.data.resolved,
                special_marks: data.data.special_marks,
                picture: data.data.picture,
                report_type: data.data.report_type,
                location: data.data.location,
                description: data.data.description
            });
        }
    }

    async function  handleDeleteButton () {
        await ServiceApi.deleteReport(Number(id))
        navigate('/reports')
    }

    function handleSubmitButton() {
        const errors = []
        if(currentFormData?.title.length === 0) {
            errors.push('Заголовок должен содержать хотя бы один символ')
        }
        else if(currentFormData?.special_marks.length === 0) {
            errors.push('Поле отличительных знаков должно содержать хотя бы один символ')
        }
        else if(currentFormData?.location.length === 0) {
            errors.push('Поле локации должно содержать хотя бы один символ')
        }
        else if(currentFormData?.description.length === 0) {
            errors.push('Поле описания должно содержать хотя бы один символ')
        }

        if(errors.length > 0) {
            setValidateErrors(errors)
            console.log(validateErrors)
            return;
        }

        async function putData () {
            if(report) {
               const response = await ServiceApi.updateReports(report.id, currentFormData!);
               if(response.status === 200){
                setReport(response.data)
               }
            }
            setIsModalOpen(false);
        }

        putData();
    }   

    useEffect(() => {
        window.scroll(0, 0);
        fetching();
    }, [])
    console.log(report);
    
    return (
        <div className={styles.wrapper}>
            {report?.picture && <Img className={styles.photo} photo={report.picture} altPhoto={altPhoto}  />}
            <h2 className={styles.title}>{report?.title}</h2>
            <p className={styles.description}>{report?.description}</p>
            <p className={styles.special_marks}>{report?.special_marks}</p>
            <div className={styles.btns}>
                <button className={styles.edit} onClick={() => setIsModalOpen(true)}>Редактировать</button>
                <button className={styles.delete} onClick={handleDeleteButton}>Удалить</button>
            </div>
            
                <Modal 
                    isOpen={isModalOpen} 
                    onClose={() => setIsModalOpen(false)}
                >
                    <h2>Изменение объявления</h2>
                    {currentFormData && <form action="" className={styles.form}>
                        <label htmlFor="title">Заголовок</label>
                            <input type="text"
                            value={currentFormData?.title}
                            onChange={(e) => setCurrentFormData({...currentFormData, title: e.target.value})}
                            />
                        <label htmlFor="special_marks">Отличнительные знаки</label>
                            <input 
                            type="text" 
                            value={currentFormData.special_marks}
                            onChange={(e) => setCurrentFormData({...currentFormData, special_marks: e.target.value})}
                            />
                        <label htmlFor="location">Место {currentFormData.report_type === 'found' ? 'нахождения' : 'пропажи'}</label>
                            <input 
                            type="text" 
                            value={currentFormData.location}
                            onChange={(e) => setCurrentFormData({...currentFormData, location: e.target.value})}
                            />
                        <label htmlFor="description">Описание</label>
                            <input 
                            type="text" 
                            value={currentFormData.description}
                            onChange={(e) => setCurrentFormData({...currentFormData, description: e.target.value})}
                            />
                        <button type="button" onClick={handleSubmitButton}>Подтвердить изменение</button>
                    </form>}
                </Modal>
            {/* Стили менять в компоненте PostReport.tsx */}
        </div>
    );
}
 
export default Report;